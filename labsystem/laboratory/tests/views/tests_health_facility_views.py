from django.utils import timezone

from labsystem.laboratory.models import Country, City, HealthFacility
from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse, resolve
from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.views.health_facility_views import HealthFacilityCreation


class DepartmentViewTests(TestCase):
    USERNAME = 'John'
    PASSWORD = '1234'
    CREATE_URL = 'health_facility/create/'
    CREATE_URL_NAME = 'health facility register'
    EDIT_URL = 'health_facility/<int:pk>/edit/'
    EDIT_URL_NAME = 'edit health facility'
    DELETE_URL = 'health_facility/<int:pk>/delete/'
    DELETE_URL_NAME = 'delete health facility'
    RESTORE_URL = 'dhealth_facility/<int:pk>/restore/'
    RESTORE_URL_NAME = 'restore health facility'
    ALL_LIST_URL_NAME = 'all health facilities'
    ALL_DELETED_LIST_URL_NAME = 'all deleted health facilities'
    NAME = 'Name'
    NAME2 = 'NameName'
    COUNTRY_CODE = 'BG'
    CITY_CODE = 1000
    VAT = 'BG1000'
    VAT2 = 'BG10002'
    COMMENTS = 'Comments'
    TEL_NUMBER = '+359555'
    EMAIL = 'department@mail.bg'
    HTTP_RESPONSE_OK = 200
    HTTP_RESPONSE_REDIRECT = 302

    def setUp(self):
        self.client = Client()
        country = Country.objects.create(
            name=self.NAME,
            code=self.COUNTRY_CODE
        )
        city = City.objects.create(
            name=self.NAME,
            post_code=self.CITY_CODE,
            municipality=self.NAME,
            province=self.NAME,
            country=country,
        )

        HealthFacility.objects.create(
            name=self.NAME,
            address=self.NAME,
            city=city,
            vat=self.VAT,
            contact_person=self.NAME,
            telephone_number=self.TEL_NUMBER,
            email=self.EMAIL,
            comments=self.COMMENTS,
        )

        HealthFacility.objects.create(
            name=self.NAME2,
            address=self.NAME,
            city=city,
            vat=self.VAT2,
            contact_person=self.NAME,
            telephone_number=self.TEL_NUMBER,
            email=self.EMAIL,
            comments=self.COMMENTS,
        )

    def test_HealthFacilityCreation_url_is_resolved(self):
        url = reverse(self.CREATE_URL_NAME)
        self.assertEquals(resolve(url).func.view_class, HealthFacilityCreation)

    def test_HealthFacilityCreation__unauthenticated_user_can_not_see_page(self):
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_HealthFacilityCreation__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test__HealthFacilityCreation__staff_user_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test__HealthFacilityCreation__deleted_staff_user_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.deleted_at = datetime.now()
        user.is_active = False
        self.client.force_login(user=user)
        user.save()
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test__HealthFacilityCreation__physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditHealthFacility__unauthenticated_user_can_not_see_page(self):
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditHealthFacility__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditHealthFacility__staff_user_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditHealthFacility__deleted_staff_user_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.deleted_at = datetime.now()
        user.is_active = False
        self.client.force_login(user=user)
        user.save()
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditAnalysisView__physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_health_facility_post__when_all_field_correct__expect_success(self):
        hf = HealthFacility.objects.last()
        city = City.objects.last()
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        get_response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': hf.pk}))
        post_response = self.client.post(
            reverse(self.DELETE_URL_NAME, kwargs={'pk': hf.pk}),
            {'name': self.NAME,
             'address': self.NAME,
             'city': city,
             'vat': self.VAT2,
             'contact_person': self.NAME,
             'telephone_number': self.TEL_NUMBER,
             'email': self.EMAIL,
             'comments': self.COMMENTS,
             })
        self.assertEqual(get_response.status_code, self.HTTP_RESPONSE_OK)
        self.assertEqual(post_response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_health_facility__unauthenticated_user_can_not_see_page(self):
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_health_facility__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_health_facility__superuser_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_health_facility__staff_but_not_superuser_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_health_facility__deleted_superuser_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.deleted_at = datetime.now()
        user.is_active = False
        user.is_superuser = True
        self.client.force_login(user=user)
        user.save()
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_health_facility__physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_health_facility_post__when_all_field_correct__expect_success(self):
        hf = HealthFacility.objects.last()
        city = City.objects.last()
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        get_response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': hf.pk}))
        post_response = self.client.post(
            reverse(self.RESTORE_URL_NAME, kwargs={'pk': hf.pk}),
            {'name': self.NAME,
             'address': self.NAME,
             'city': city,
             'vat': self.VAT2,
             'contact_person': self.NAME,
             'telephone_number': self.TEL_NUMBER,
             'email': self.EMAIL,
             'comments': self.COMMENTS,
             })
        self.assertEqual(get_response.status_code, self.HTTP_RESPONSE_OK)
        self.assertEqual(post_response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_health_facility__unauthenticated_user_can_not_see_page(self):
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_health_facility__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_health_facility__superuser_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_health_facility_but_not_superuser_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_health_facility__deleted_superuser_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.deleted_at = datetime.now()
        user.is_active = False
        user.is_superuser = True
        self.client.force_login(user=user)
        user.save()
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_health_facility__physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_HealthFacilityListView__when_health_facilities_are_not_deleted__expect_get_proper_context_data(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        hf1 = HealthFacility.objects.first()
        hf2 = HealthFacility.objects.last()
        response = self.client.get(reverse(self.ALL_LIST_URL_NAME))
        context = response.context
        self.assertIn(hf1, context['all_facilities'])
        self.assertIn(hf2, context['all_facilities'])

    def test_HealthFacilityListView__when_one_health_facility_is_deleted_and_one_is_not__expect_get_proper_context_data_with_only_nondeleted_department(
            self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        hf1 = HealthFacility.objects.first()
        hf1.deleted_at = timezone.now()
        hf1.save()
        hf2 = HealthFacility.objects.last()
        response = self.client.get(reverse(self.ALL_LIST_URL_NAME))
        context = response.context
        self.assertNotIn(hf1, context['all_facilities'])
        self.assertIn(hf2, context['all_facilities'])

    def test_DeletedHealthFacilityListView__when_all_health_facilities_are_deleted__expect_get_proper_context_data(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        hf1 = HealthFacility.objects.first()
        hf1.deleted_at = timezone.now()
        hf1.save()
        hf2 = HealthFacility.objects.last()
        hf2.deleted_at = timezone.now()
        hf2.save()
        response = self.client.get(reverse(self.ALL_DELETED_LIST_URL_NAME))
        context = response.context
        self.assertIn(hf1, context['all_deleted_facilities'])
        self.assertIn(hf2, context['all_deleted_facilities'])

    def test_DeletedHealthFacilityListView__when_one_health_facility_is_deleted_and_one_is_not__expect_get_proper_context_data_with_only_nondeleted_department(
            self):
        user = LimsUser.objects.create_staff_user(self.USERNAME, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        hf1 = HealthFacility.objects.first()
        hf1.deleted_at = timezone.now()
        hf1.save()
        hf2 = HealthFacility.objects.last()
        response = self.client.get(reverse(self.ALL_DELETED_LIST_URL_NAME))
        context = response.context
        self.assertNotIn(hf2, context['all_deleted_facilities'])
        self.assertIn(hf1, context['all_deleted_facilities'])
