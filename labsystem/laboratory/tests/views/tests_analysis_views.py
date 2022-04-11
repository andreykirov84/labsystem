from datetime import datetime
from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone

from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.models import Analysis
from labsystem.laboratory.views.analysis_views import CreateAnalysisView


class AnalysisViewTests(TestCase):
    CREATE_TEMPLATE = 'labsystem/templates/laboratory/analysis_field/analysis_field_create.html'
    USERNAME = 'John'
    PASSWORD = '1234'
    CREATE_URL = 'analyses/create/'
    CREATE_URL_NAME = 'create analysis'
    EDIT_URL = 'analyses/<int:pk>/edit/'
    EDIT_URL_NAME = 'edit analysis'
    ALL_LIST_URL_NAME = 'all analyses'
    ALL_DELETED_LIST_URL_NAME = 'all deleted analyses'
    NAME = 'Name'
    NAME2 = 'NameName'
    VALUE = 1
    COMMENT = 'Comment'
    DESCRIPTION = 'Description'
    CURRENCY = 'EUR'
    PRICE = 1
    TAT = 1


    def setUp(self):
        Analysis.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
            currency=self.CURRENCY,
            price=self.PRICE,
            tat=self.TAT,
        )

        Analysis.objects.create(
            name=self.NAME2,
            description=self.DESCRIPTION,
            currency=self.CURRENCY,
            price=self.PRICE,
            tat=self.TAT,
        )

    def test_CreateAnalysisView_url_is_resolved(self):
        url = reverse(self.CREATE_URL_NAME)
        self.assertEquals(resolve(url).func.view_class, CreateAnalysisView)

    def test_CreateAnalysisView__unauthenticated_user_can_not_see_page(self):
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, 200)

    def test_CreateAnalysisView__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, 200)

    def test__CreateAnalysisView__staff_user_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertEqual(response.status_code, 200)

    def test__CreateAnalysisView__deleted_staff_user_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.deleted_at = datetime.now()
        user.is_active = False
        self.client.force_login(user=user)
        user.save()
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, 200)

    def test__CreateAnalysisView__physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, 200)

    def test_EditAnalysisFieldView_post__when_all_field_correct__expect_success(self):
        a = Analysis.objects.first()
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        get_response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': a.pk}))
        post_response = self.client.post(
            reverse(self.EDIT_URL_NAME, kwargs={'pk': a.pk}),
            {'name': self.NAME,
             'description': self.DESCRIPTION,
             'currency': self.CURRENCY,
             'price': self.PRICE,
             'tat': self.TAT,
             })
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(post_response.status_code, 302)

    def test_EditAnalysisView__unauthenticated_user_can_not_see_page(self):
        a = Analysis.objects.first()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': a.pk}))
        self.assertNotEqual(response.status_code, 200)

    def test_EditAnalysisView__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        a = Analysis.objects.first()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': a.pk}))
        self.assertNotEqual(response.status_code, 200)

    def test_EditAnalysisView__staff_user_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        a = Analysis.objects.first()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': a.pk}))
        self.assertEqual(response.status_code, 200)

    def test__EditAnalysisView___deleted_staff_user_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.deleted_at = datetime.now()
        user.is_active = False
        self.client.force_login(user=user)
        user.save()
        a = Analysis.objects.first()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': a.pk}))
        self.assertNotEqual(response.status_code, 200)

    def test__EditAnalysisView___physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        a = Analysis.objects.first()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': a.pk}))
        self.assertNotEqual(response.status_code, 200)








    def test_AnalysesListView__when_all_analyses_are_not_deleted__expect_get_proper_context_data(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        d1 = Analysis.objects.first()
        d2 = Analysis.objects.last()
        response = self.client.get(reverse(self.ALL_LIST_URL_NAME))
        context = response.context
        self.assertIn(d1, context['all_analyses'])
        self.assertIn(d2, context['all_analyses'])

    def test_AnalysisListView__when_one_analysis_is_deleted_and_one_is_not__expect_get_proper_context_data_with_only_nondeleted_analysis(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        d1 = Analysis.objects.first()
        d1.deleted_at = timezone.now()
        d1.save()
        d2 = Analysis.objects.last()
        response = self.client.get(reverse(self.ALL_LIST_URL_NAME))
        context = response.context
        self.assertNotIn(d1, context['all_analyses'])
        self.assertIn(d2, context['all_analyses'])

    def test_DeletedAnalysisListView__when_all_analyses_are_not_deleted__expect_get_proper_context_data(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        d1 = Analysis.objects.first()
        d2 = Analysis.objects.last()
        response = self.client.get(reverse(self.ALL_DELETED_LIST_URL_NAME))
        context = response.context
        self.assertNotIn(d1, context['all_analyses'])
        self.assertNotIn(d2, context['all_analyses'])

    def test_DeletedDepartmentsListView__when_one_analysis_is_deleted_and_one_is_not__expect_get_proper_context_data_with_only_nondeleted_department(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        d1 = Analysis.objects.first()
        d1.deleted_at = timezone.now()
        d1.save()
        d2 = Analysis.objects.last()
        response = self.client.get(reverse(self.ALL_DELETED_LIST_URL_NAME))
        context = response.context
        self.assertNotIn(d2, context['all_analyses'])
        self.assertIn(d1, context['all_analyses'])



