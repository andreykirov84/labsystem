from django.utils import timezone

from labsystem.laboratory.models import Country, City, HealthFacility, PidType, Sex, Specialty, Position, Department, \
    Profile
from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from labsystem.auth_app.models import LimsUser


class DepartmentViewTests(TestCase):
    USERNAME = 'John'
    PASSWORD = '1234'
    CREATE_URL = 'patients/create/<int:pk>/profile/'
    CREATE_URL_NAME = 'create patient'
    EDIT_URL = 'patients/<int:pk>/edit/'
    EDIT_URL_NAME = 'edit patient'
    DELETE_URL = 'patients/<int:pk>/delete/'
    DELETE_URL_NAME = 'delete patient'
    RESTORE_URL = 'patients/<int:pk>/restore/'
    RESTORE_URL_NAME = 'restore patient'
    ALL_LIST_URL_NAME = 'all patients'
    ALL_DELETED_LIST_URL_NAME = 'all deleted patients'
    NAME = 'Name'
    NAME2 = 'NameName'
    NAME3 = 'NameA'
    COUNTRY_CODE = 'BG'
    CITY_CODE = 1000
    VAT = 'BG1000'
    VAT2 = 'BG10002'
    COMMENTS = 'Comments'
    DESCRIPTION = 'Description'
    TEL_NUMBER = '+359555'
    EMAIL = 'department@mail.bg'
    PID = 'EGN'
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
        hf = HealthFacility.objects.create(
            name=self.NAME,
            address=self.NAME,
            city=city,
            vat=self.VAT,
            contact_person=self.NAME,
            telephone_number=self.TEL_NUMBER,
            email=self.EMAIL,
            comments=self.COMMENTS,
        )
        pt = PidType.objects.create(
            name=self.PID,
        )
        sex = Sex.objects.create(
            name=self.NAME,
        )
        speciality = Specialty.objects.create(
            name=self.NAME,
        )
        position = Position.objects.create(
            name=self.NAME,
        )
        department = Department.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
            telephone_number=self.TEL_NUMBER,
            email=self.EMAIL
        )
        user1 = LimsUser.objects.create(
            username=self.NAME,
            is_staff=True,
            is_physician=False,
            is_patient=False,
        )
        user2 = LimsUser.objects.create(
            username=self.NAME3,
            is_staff=True,
            is_physician=False,
            is_patient=False,
        )

        Profile.objects.create(
            pid=self.PID,
            pid_type=pt,
            first_name=self.NAME,
            middle_name=self.NAME,
            last_name=self.NAME,
            date_of_birth='1980-03-03',
            sex=sex,
            telephone_number=self.TEL_NUMBER,
            email=self.EMAIL,
            address=self.NAME,
            city=city,
            clinical_data=self.NAME,
            specialty=speciality,
            health_facility=hf,
            position=position,
            department=department,
            salary=100,
            comments=self.COMMENTS,
            user=user1
        )

        Profile.objects.create(
            pid='pid2',
            pid_type=pt,
            first_name=self.NAME,
            middle_name=self.NAME,
            last_name=self.NAME,
            date_of_birth='1980-03-03',
            sex=sex,
            telephone_number=self.TEL_NUMBER,
            email=self.EMAIL,
            address=self.NAME,
            city=city,
            clinical_data=self.NAME,
            specialty=speciality,
            health_facility=hf,
            position=position,
            department=department,
            salary=100,
            comments=self.COMMENTS,
            user=user2
        )

    def test_EditPatientView__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.NAME2, self.PASSWORD)
        self.client.force_login(user=user)
        p = Profile.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': p.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditPatientView__staff_user_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.NAME2, self.PASSWORD)
        self.client.force_login(user=user)
        p = Profile.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': p.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditPatientView__physician_user_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.NAME2, self.PASSWORD)
        self.client.force_login(user=user)
        p = Profile.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': p.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_patient_view__unauthenticated_user_can_not_see_page(self):
        p = Profile.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': p.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_patient_view__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME, self.PASSWORD)
        self.client.force_login(user=user)
        hf = HealthFacility.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': hf.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_patient_view__superuser_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.NAME2, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        p = Profile.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': p.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_patient_view__staff_but_not_superuser_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.NAME2, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        p = Profile.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': p.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_patient_view__deleted_superuser_can_not_see_page(self):
        user = LimsUser.objects.create_staff_user(self.NAME2, self.PASSWORD)
        user.deleted_at = datetime.now()
        user.is_active = False
        user.is_superuser = True
        self.client.force_login(user=user)
        user.save()
        p = Profile.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': p.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_delete_patient_view__physician_user_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.NAME2, self.PASSWORD)
        self.client.force_login(user=user)
        p = Profile.objects.last()
        response = self.client.get(reverse(self.DELETE_URL_NAME, kwargs={'pk': p.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_restore_patient_view__superuser_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.NAME2, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        p = Profile.objects.last()
        response = self.client.get(reverse(self.RESTORE_URL_NAME, kwargs={'pk': p.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_PatientsListView_view__when_profiles_are_not_deleted__expect_get_proper_context_data(self):
        expected_context_length = 2
        user = LimsUser.objects.create_staff_user(self.NAME2, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        p1 = Profile.objects.first()
        p2 = Profile.objects.last()
        response = self.client.get(reverse(self.ALL_LIST_URL_NAME))
        context = response.context
        self.assertEqual(len(context), expected_context_length)
        
    def test_DeletedPatientsListView__when_all_profiles_are_deleted__expect_get_proper_context_data(self):
        expected_context_length = 2
        user = LimsUser.objects.create_staff_user(self.NAME2, self.PASSWORD)
        user.is_superuser = True
        self.client.force_login(user=user)
        p1 = Profile.objects.first()
        p1.deleted_at = timezone.now()
        p1.save()
        p2 = Profile.objects.last()
        p2.deleted_at = timezone.now()
        p2.save()
        response = self.client.get(reverse(self.ALL_DELETED_LIST_URL_NAME))
        context = response.context
        self.assertEqual(len(context), expected_context_length)


