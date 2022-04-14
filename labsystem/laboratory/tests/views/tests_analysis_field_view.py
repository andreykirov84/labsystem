from datetime import datetime
from django.test import TestCase
from django.urls import reverse, resolve
from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.models import AnalysisField
from labsystem.laboratory.views.analysis_field_views import CreateAnalysisFieldView


class AnalysisFieldViewTests(TestCase):
    CREATE_TEMPLATE = 'labsystem/templates/laboratory/analysis_field/analysis_field_create.html'
    USERNAME = 'John'
    USERNAME2 = 'Johnn'
    PASSWORD = '1234'
    CREATE_URL = 'analysis_fields/create/'
    CREATE_URL_NAME = 'create analysis field'
    EDIT_URL = 'analysis_fields/<int:pk>/edit/'
    EDIT_URL_NAME = 'edit analysis field'
    NAME = 'Name'
    UNIT = 'IU/l'
    VALUE = 1.00
    COMMENT = 'Comment'
    NEW_NAME = 'New Name'
    NEW_UNIT = 'New Unit'
    NEW_VALUE = 'New Value'
    NEW_COMMENT = 'New Comment'

    def setUp(self):
        AnalysisField.objects.create(
            name=self.NAME,
            unit=self.UNIT,
            male_min=self.VALUE,
            male_max=self.VALUE,
            female_min=self.VALUE,
            female_max=self.VALUE,
            comment=self.COMMENT,
        )

        LimsUser.objects.create_staff_user(username=self.USERNAME, password=self.PASSWORD)

    def test_CreateAnalysisFieldView_post__when_all_field_correct__expect_create_instance(self):
        self.client.post(self.CREATE_URL,
                         {'name': self.NAME,
                          'unit': self.UNIT,
                          'male_min': self.VALUE,
                          'male_max': self.VALUE,
                          'female_min': self.VALUE,
                          'female_max': self.VALUE,
                          'comment': self.COMMENT,
                          })
        self.assertEqual(AnalysisField.objects.last().name, self.NAME)
        self.assertEqual(AnalysisField.objects.last().unit, self.UNIT)
        self.assertEqual(AnalysisField.objects.last().male_min, self.VALUE)
        self.assertEqual(AnalysisField.objects.last().male_max, self.VALUE)
        self.assertEqual(AnalysisField.objects.last().female_min, self.VALUE)
        self.assertEqual(AnalysisField.objects.last().female_max, self.VALUE)
        self.assertEqual(AnalysisField.objects.last().comment, self.COMMENT)

    def test_CreateAnalysisFieldView_url_is_resolved(self):
        url = reverse(self.CREATE_URL_NAME)
        self.assertEquals(resolve(url).func.view_class, CreateAnalysisFieldView)

    def test_CreateAnalysisFieldView__unauthenticated_user_can_not_see_page(self):
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, 200)

    def test_authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME2, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, 200)

    def test_CreateAnalysisFieldView__staff_user_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME2, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertEqual(response.status_code, 200)

    def test_CreateAnalysisFieldView__deleted_staff_user_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME2, self.PASSWORD)
        user.deleted_at = datetime.now()
        user.is_active = False
        self.client.force_login(user=user)
        user.save()
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, 200)

    def test_CreateAnalysisFieldView__physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_physician_user(self.USERNAME2, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, 200)

    def test_EditAnalysisFieldView_post__when_all_field_correct__expect_success(self):
        af = AnalysisField.objects.first()
        user = LimsUser.objects.first()
        self.client.force_login(user=user)
        get_response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': af.pk}))
        post_response = self.client.post(
            reverse(self.EDIT_URL_NAME, kwargs={'pk': af.pk}),
            {'name': self.NEW_NAME,
             'unit': self.NEW_UNIT,
             'male_min': self.NEW_VALUE,
             'male_max': self.NEW_VALUE,
             'female_min': self.NEW_VALUE,
             'female_max': self.NEW_VALUE,
             'comment': self.NEW_COMMENT,
             })
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(post_response.status_code, 200)




