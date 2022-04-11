from django.utils import timezone

from labsystem.laboratory.models import Department
from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse, resolve
from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.views.department_views import DepartmentCreation


class DepartmentViewTests(TestCase):
    USERNAME = 'John'
    PASSWORD = '1234'
    CREATE_URL = 'department/create/'
    CREATE_URL_NAME = 'department register'
    EDIT_URL = 'department/<int:pk>/edit/'
    EDIT_URL_NAME = 'edit department'
    DELETE_URL = 'department/<int:pk>/delete/'
    DELETE_URL_NAME = 'delete department'
    RESTORE_URL = 'department/<int:pk>/restore/'
    RESTORE_URL_NAME = 'restore department'
    ALL_LIST_URL_NAME = 'all departments'
    ALL_DELETED_LIST_URL_NAME = 'all deleted departments'
    NAME = 'Name'
    NAME_2 = 'NameName'
    DESCRIPTION = 'Description'
    TEL_NUMBER = '+359555'
    EMAIL = 'department@mail.bg'
    HTTP_RESPONSE_OK = 200
    HTTP_RESPONSE_REDIRECT = 302

    def setUp(self):
        self.client = Client()
        Department.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
            telephone_number=self.TEL_NUMBER,
            email=self.EMAIL
        )
        Department.objects.create(
            name=self.NAME_2,
            description=self.DESCRIPTION,
            telephone_number=self.TEL_NUMBER,
            email=self.EMAIL
        )

    def test_CreatDepartmentView_url_is_resolved(self):
        url = reverse(self.CREATE_URL_NAME)
        self.assertEquals(resolve(url).func.view_class, DepartmentCreation)

    def test_CreatDepartmentView__unauthenticated_user_can_not_see_page(self):
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_CreatDepartmentView__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test__CreatDepartmentView__staff_user_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test__CreatDepartmentView__deleted_staff_user_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.deleted_at = datetime.now()
        user.is_active = False
        self.client.force_login(user=user)
        user.save()
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test__CreatDepartmentView__physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditAnalysisView__unauthenticated_user_can_not_see_page(self):
        d = Department.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditAnalysisView__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        d = Department.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditAnalysisView__staff_user_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        d = Department.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': d.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test__EditAnalysisView___deleted_staff_user_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.deleted_at = datetime.now()
        user.is_active = False
        self.client.force_login(user=user)
        user.save()
        d = Department.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test__EditAnalysisView___physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        d = Department.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_department_post__when_all_field_correct__expect_success(self):
        d = Department.objects.last()
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        get_response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': d.pk}))
        post_response = self.client.post(
            reverse(self.DELETE_URL_NAME, kwargs={'pk': d.pk}),
            {'name': self.NAME,
             'description': self.DESCRIPTION,
             'telephone_number': self.TEL_NUMBER,
             'email': self.EMAIL,
             })
        self.assertEqual(get_response.status_code, self.HTTP_RESPONSE_REDIRECT)
        self.assertEqual(post_response.status_code, self.HTTP_RESPONSE_REDIRECT)

    def test_delete_department__unauthenticated_user_can_not_see_page(self):
        d = Department.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_department__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        d = Department.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_department__superuser_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        d = Department.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': d.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_REDIRECT)

    def test_delete_department__staff_but_not_superuser_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        d = Department.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_department__deleted_superuser_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.deleted_at = datetime.now()
        user.is_active = False
        user.is_superuser = True
        self.client.force_login(user=user)
        user.save()
        d = Department.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_department__physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        d = Department.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_department_post__when_all_field_correct__expect_success(self):
        d = Department.objects.last()
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        get_response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': d.pk}))
        post_response = self.client.post(
            reverse(self.RESTORE_URL_NAME, kwargs={'pk': d.pk}),
            {'name': self.NAME,
             'description': self.DESCRIPTION,
             'telephone_number': self.TEL_NUMBER,
             'email': self.EMAIL,
             })
        self.assertEqual(get_response.status_code, self.HTTP_RESPONSE_REDIRECT)
        self.assertEqual(post_response.status_code, self.HTTP_RESPONSE_REDIRECT)

    def test_restore_department__unauthenticated_user_can_not_see_page(self):
        d = Department.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_department__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        d = Department.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_department__superuser_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        d = Department.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': d.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_REDIRECT)

    def test_restore_department__staff_but_not_superuser_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        d = Department.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_department__deleted_superuser_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.deleted_at = datetime.now()
        user.is_active = False
        user.is_superuser = True
        self.client.force_login(user=user)
        user.save()
        d = Department.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_department__physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        d = Department.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': d.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_DepartmentsListView__when_departments_are_not_deleted__expect_get_proper_context_data(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        d1 = Department.objects.first()
        d2 = Department.objects.last()
        response = self.client.get(reverse(self.ALL_LIST_URL_NAME))
        context = response.context
        self.assertIn(d1, context['all_departments'])
        self.assertIn(d2, context['all_departments'])

    def test_DepartmentsListView__when_one_department_is_deleted_and_one_is_not__expect_get_proper_context_data_with_only_nondeleted_department(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        d1 = Department.objects.first()
        d1.deleted_at = timezone.now()
        d1.save()
        d2 = Department.objects.last()
        response = self.client.get(reverse(self.ALL_LIST_URL_NAME))
        context = response.context
        self.assertNotIn(d1, context['all_departments'])
        self.assertIn(d2, context['all_departments'])

    def test_DeletedDepartmentsListView__when_all_departments_are_deleted__expect_get_proper_context_data(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        d1 = Department.objects.first()
        d1.deleted_at = timezone.now()
        d1.save()
        d2 = Department.objects.last()
        d2.deleted_at = timezone.now()
        d2.save()
        response = self.client.get(reverse(self.ALL_DELETED_LIST_URL_NAME))
        context = response.context
        self.assertIn(d1, context['all_deleted_departments'])
        self.assertIn(d2, context['all_deleted_departments'])

    def test_DeletedDepartmentsListView__when_one_department_is_deleted_and_one_is_not__expect_get_proper_context_data_with_only_nondeleted_department(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        d1 = Department.objects.first()
        d1.deleted_at = timezone.now()
        d1.save()
        d2 = Department.objects.last()
        response = self.client.get(reverse(self.ALL_DELETED_LIST_URL_NAME))
        context = response.context
        self.assertNotIn(d2, context['all_deleted_departments'])
        self.assertIn(d1, context['all_deleted_departments'])
