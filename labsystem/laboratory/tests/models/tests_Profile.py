from django.core.exceptions import ValidationError
from django.test import TestCase

from labsystem.laboratory.models import Profile, PidType, Sex, Specialty, HealthFacility, Position, Department, City, \
    Country


class ProfileTests(TestCase):
    pid_type = PidType('EGN')
    sex = Sex('Male')
    country = Country(
        name='Bulgaria',
        code='BG'
    )
    city = City(
        name='City',
        post_code='1111',
        municipality='Municipality',
        province='Province',
        country=country,
    )
    specialty = Specialty('speciality')
    health_facility = HealthFacility(
        name='Name',
        address='Address',
        vat='BG111',
        contact_person='Contact Person'
    )
    position = Position('Position')
    department = Department('Department')

    VALID_PROFILE_DATA = {
        'pid': '1111111111',
        'pid_type': pid_type,
        'first_name': 'Bai',
        'middle_name': 'Ivan',
        'last_name': 'Ivanov',
        'date_of_birth': '2022-04-04',
        'sex': sex,
        'telephone_number': '+359898888888',
        'email': 'bai_ivan@gmail.comm',
        'address': '1 Somewhere str.',
        'city': city,
        'clinical_data': 'Healthy person',
        'specialty': specialty,
        'health_facility': health_facility,
        'position': position,
        'department': department,
        'salary': 1000,
        'comments': 'valid data comment',
    }


    # @classmethod
    # def setUpTestData(cls):
    #     # Set up data for the whole TestCase
    #     # cls.foo = Foo.objects.create(bar="Test")
    #
    #     cls.pid_type = PidType('EGN')
    #     cls.sex = Sex('Sex')
    #     cls.country = Country(
    #         name='Bulgaria',
    #         code='BG'
    #     )
    #     cls.city = City(
    #         name='City',
    #         post_code='1111',
    #         municipality='Municipality',
    #         province='Province',
    #         country=cls.country,
    #     )
    #     cls.specialty = Specialty('speciality')
    #     cls.health_facility = HealthFacility(
    #         name='Name',
    #         address='Address',
    #         vat='BG111',
    #         contact_person='Contact Person'
    #     )
    #     cls.position = Position('Position')
    #     cls.department = Department('Department')
    #
    #     cls.VALID_PROFILE_DATA = {
    #         'pid': 1,
    #         'pid_type': cls.pid_type,
    #         'first_name': 'Bai',
    #         'middle_name': 'Ivan',
    #         'last_name': 'Ivanov',
    #         'date_of_birth': '2022-04-04',
    #         'sex': cls.sex,
    #         'telephone_number': '+359898888888',
    #         'email': 'bai_ivan@gmail.comm',
    #         'address': '1 Somewhere str.',
    #         'city': cls.city,
    #         'clinical_data': 'Healthy person',
    #         'specialty': cls.specialty,
    #         'health_facility': cls.health_facility,
    #         'position': cls.position,
    #         'department': cls.department,
    #         'salary': 1000,
    #         'comments': 'valid data comment',
    #     }

    def test_profile_create__when_first_name_contains_only_Letters__expect_success(self):
        pass
        # test_first_name = 'Pesho'
        # profile = Profile(
        #     pid=self.VALID_PROFILE_DATA['pid'],
        #     pid_type=self.VALID_PROFILE_DATA['pid_type'],
        #     first_name=test_first_name,
        #     middle_name=self.VALID_PROFILE_DATA['middle_name'],
        #     last_name=self.VALID_PROFILE_DATA['last_name'],
        #     date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
        #     sex=self.VALID_PROFILE_DATA['sex'],
        #     telephone_number=self.VALID_PROFILE_DATA['telephone_number'],
        #     email=self.VALID_PROFILE_DATA['email'],
        #     address=self.VALID_PROFILE_DATA['address'],
        #     city=self.VALID_PROFILE_DATA['city'],
        #     clinical_data=self.VALID_PROFILE_DATA['clinical_data'],
        #     specialty=self.VALID_PROFILE_DATA['specialty'],
        #     health_facility=self.VALID_PROFILE_DATA['health_facility'],
        #     position=self.VALID_PROFILE_DATA['position'],
        #     department=self.VALID_PROFILE_DATA['department'],
        #     salary=self.VALID_PROFILE_DATA['salary'],
        #     comments=self.VALID_PROFILE_DATA['comments'],
        # )
        #
        # self.assertIsNone(profile.pk)

    def test_profile_create__when_first_name_contains_a_digit__expect_failure(self):
        pass
        # test_first_name = 'Pesho1'
        # profile = Profile(
        #     pid=self.VALID_PROFILE_DATA['pid'],
        #     pid_type=self.VALID_PROFILE_DATA['pid_type'],
        #     first_name=test_first_name,
        #     middle_name=self.VALID_PROFILE_DATA['middle_name'],
        #     last_name=self.VALID_PROFILE_DATA['last_name'],
        #     date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
        #     sex=self.VALID_PROFILE_DATA['sex'],
        #     telephone_number=self.VALID_PROFILE_DATA['telephone_number'],
        #     email=self.VALID_PROFILE_DATA['email'],
        #     address=self.VALID_PROFILE_DATA['address'],
        #     city=self.VALID_PROFILE_DATA['city'],
        #     clinical_data=self.VALID_PROFILE_DATA['clinical_data'],
        #     specialty=self.VALID_PROFILE_DATA['specialty'],
        #     health_facility=self.VALID_PROFILE_DATA['health_facility'],
        #     position=self.VALID_PROFILE_DATA['position'],
        #     department=self.VALID_PROFILE_DATA['department'],
        #     salary=self.VALID_PROFILE_DATA['salary'],
        #     comments=self.VALID_PROFILE_DATA['comments'],
        # )
        #
        # with self.assertRaises(ValidationError) as context:
        #     profile.full_clean()  # This is called in ModelForms implicitly, but here we need to call it explicitly
        #     profile.save()
        #
        # self.assertIsNone(context.exception)

    def test_profile_create__when_first_name_contains_a_dolar_sign__expect_failure(self):
        pass

    def test_profile_create__when_first_name_contains_a_space__expect_failure(self):
        pass

    def test_profile_full_name_property__when_have_all_names__expect_correct_full_name(self):
        pass
        # profile = Profile(**self.VALID_PROFILE_DATA)
        # expected_full_name = f'{self.VALID_PROFILE_DATA["first_name"]} {self.VALID_PROFILE_DATA["middle_name"]} {self.VALID_PROFILE_DATA["last_name"]} '
        # self.assertEqual(expected_full_name, profile.full_name)
