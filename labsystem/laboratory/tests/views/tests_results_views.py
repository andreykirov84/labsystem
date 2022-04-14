from labsystem.laboratory.models import Country, City, HealthFacility, PidType, Sex, Specialty, Position, Department, \
    Analysis, SampleType, ResultStatus, Profile, Result
from django.test import TestCase, Client
from django.urls import reverse, resolve
from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.views.results_views import CreateResultView


class DepartmentViewTests(TestCase):
    USERNAME = 'John'
    USERNAME2 = 'John2'
    PASSWORD = '1234'
    CREATE_URL = 'patient/<int:pk>/result/create/'
    CREATE_URL_NAME = 'add result to patient'
    EDIT_URL = 'patient/<int:pk>/result/edit/'
    EDIT_URL_NAME = 'edit result'
    ALL_LIST_URL_NAME = 'all patient specific results'
    NAME = 'Name'
    NAME2 = 'NameName'
    VALUE = 1
    COUNTRY_CODE = 'BG'
    CITY_CODE = 1000
    VAT = 'BG1000'
    VAT2 = 'BG10002'
    COMMENT = 'Comment'
    DESCRIPTION = 'Description'
    TEL_NUMBER = '+359555'
    EMAIL = 'department@mail.bg'
    PRICE = 100
    CURRENCY = 'EUR'
    TAT = 1
    POSITIVE_VALUE = 1
    ZERO_VALUE = 0
    NEGATIVE_VALUE = -1
    PAYMENT_TYPE = 'Cash payment'
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
            comments=self.COMMENT,
        )
        pt = PidType.objects.create(
            name='EGN',
        )
        sex = Sex.objects.create(
            name='Male',
        )
        speciality = Specialty.objects.create(
            name='Cardiology',
        )
        position = Position.objects.create(
            name='CTO',
        )
        department = Department.objects.create(
            name='IT',
            description='IT',
            telephone_number='+359555555',
            email='department@mail.bg'
        )
        user = LimsUser.objects.create(
            username='patient',
            is_staff=False,
            is_physician=False,
            is_patient=True,
        )

        analysis = Analysis.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
            currency=self.CURRENCY,
            price=self.PRICE,
            tat=self.TAT,
        )

        sample_type = SampleType.objects.create(
            name=self.NAME,
        )

        status = ResultStatus.objects.create(
            name='Ready',
        )

        profile = Profile.objects.create(
            pid=1111,
            pid_type=pt,
            first_name='FirstName',
            middle_name='MiddleName',
            last_name='LastName',
            date_of_birth='1980-03-03',
            sex=sex,
            telephone_number='+359888888',
            email='mail@mail.bg',
            address='1 Address str',
            city=city,
            clinical_data='Clinical Data',
            specialty=speciality,
            health_facility=hf,
            position=position,
            department=department,
            salary=100,
            comments='Comment',
            user=user
        )

        Result.objects.create(
            patient=profile,
            referring_physician=profile,
            analysis=analysis,
            sample_type=sample_type,
            status=status,
            analysis_price=self.POSITIVE_VALUE,
            currency=self.CURRENCY,
            payment_amount=self.POSITIVE_VALUE,
            payment_type=self.PAYMENT_TYPE,
        )

        Result.objects.create(
            patient=profile,
            referring_physician=profile,
            analysis=analysis,
            sample_type=sample_type,
            status=status,
            analysis_price=self.POSITIVE_VALUE,
            currency=self.CURRENCY,
            payment_amount=self.POSITIVE_VALUE,
            payment_type=self.PAYMENT_TYPE,
        )

    def test_CreateResultView_url_is_resolved(self):
        user = LimsUser.objects.first()
        url = reverse(self.CREATE_URL_NAME,  kwargs={'pk': user.pk})
        self.assertEquals(resolve(url).func.view_class, CreateResultView)

    def test_CreateResultView__unauthenticated_user_can_not_see_page(self):
        user = LimsUser.objects.first()
        response = self.client.get(reverse(self.CREATE_URL_NAME, kwargs={'pk': user.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_CreateResultView__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME2, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME, kwargs={'pk': user.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test__HealthFacilityCreation__physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_physician_user(self.USERNAME2, self.PASSWORD)
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.CREATE_URL_NAME, kwargs={'pk': user.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditResultView__unauthenticated_user_can_not_see_page(self):
        r = Result.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': r.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditResultView__authenticated_patient_user_can_not_see_page(self):
        user = LimsUser.objects.create_patient_user(self.USERNAME2, self.PASSWORD)
        self.client.force_login(user=user)
        r = Result.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': r.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditResultView__staff_user_can_see_page(self):
        user = LimsUser.objects.create_staff_user(self.USERNAME2, self.PASSWORD)
        self.client.force_login(user=user)
        r = Result.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': r.pk}))
        self.assertEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_EditAnalysisView__physician_user_can_not_see_page(self):
        user = LimsUser.objects.create_physician_user(self.USERNAME2, self.PASSWORD)
        self.client.force_login(user=user)
        r = Result.objects.last()
        response = self.client.get(reverse(self.EDIT_URL_NAME, kwargs={'pk': r.pk}))
        self.assertNotEqual(response.status_code, self.HTTP_RESPONSE_OK)

    def test_PatientSpecificResultListView__when_all_results_belong_to_same_profile__expect_get_proper_context_data(self):
        expected_context_length = 2
        profile = Profile.objects.first()
        user = profile.user
        user_is_staff = True
        user.is_superuser = True
        user.save()
        self.client.force_login(user=user)
        response = self.client.get(reverse(self.ALL_LIST_URL_NAME, kwargs={'pk': user.pk}))
        context = response.context
        self.assertEqual(len(context), expected_context_length)
