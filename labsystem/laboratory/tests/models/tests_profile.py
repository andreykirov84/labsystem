from django.core.exceptions import ValidationError
from django.test import TestCase
import random
from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.models import Profile, PidType, Sex, Specialty, HealthFacility, Position, Department, City, \
    Country


class ProfileTests(TestCase):
    CORRECT_NAME = 'Gosho'
    NAME_CONTAINING_NUMBER = 'Gosho1'
    NAME_CONTAINING_UNDERSCORE = 'Gosho_'
    NAME_CONTAINING_DASH = 'Gosho-'
    NAME_CONTAINING_SPACE = 'Gosho Gosho'
    def setUp(self):
        country = Country.objects.create(name='Bulgaria', code='BG')
        city = City.objects.create(
            name='Sofia',
            post_code=1000,
            municipality='Sofia',
            province='Sofia',
            country=country,
        )
        hf = HealthFacility.objects.create(
            name='Name',
            address='Address',
            city=city,
            vat='BG11111',
            contact_person='John Doe',
            telephone_number='+359111',
            email='hf_contact@mail.bg',
            comments='Comments',
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
        patient_user = LimsUser.objects.create(
            username='patient',
            is_staff=False,
            is_physician=False,
            is_patient=True,
        )

        physician_user = LimsUser.objects.create(
            username='physician',
            is_staff=False,
            is_physician=True,
            is_patient=False,
        )

        staff_user = LimsUser.objects.create(
            username='staff',
            is_staff=True,
            is_physician=False,
            is_patient=False,
        )
        users = (patient_user, physician_user, staff_user)
        for user in users:
            Profile.objects.create(
                pid=random.randint(1000, 20000),
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

    def test_profile_property_is_staff__when_user_register_as_staff__expect_is_staff_is_true(self):
        profile = Profile.objects.get(user__username='staff')
        actual = profile.is_staff
        self.assertTrue(actual)

    def test_profile_property_is_patient__when_user_register_as_staff__expect_is_patient_is_false(self):
        profile = Profile.objects.get(user__username='staff')
        actual = profile.is_patient
        self.assertFalse(actual)

    def test_profile_property_is_physician__when_user_register_as_staff__expect_is_physician_is_false(self):
        profile = Profile.objects.get(user__username='staff')
        actual = profile.is_physician
        self.assertFalse(actual)

    def test_profile_property_is_staff__when_user_register_as_patient__expect_is_staff_is_false(self):
        profile = Profile.objects.get(user__username='patient')
        actual = profile.is_staff
        self.assertFalse(actual)

    def test_profile_property_is_patient__when_user_register_as_patient__expect_is_patient_is_true(self):
        profile = Profile.objects.get(user__username='patient')
        actual = profile.is_patient
        self.assertTrue(actual)

    def test_profile_property_is_physician__when_user_register_as_patient__expect_is_physician_is_false(self):
        profile = Profile.objects.get(user__username='patient')
        actual = profile.is_physician
        self.assertFalse(actual)

    def test_profile_property_is_staff__when_user_register_as_physician__expect_is_staff_is_false(self):
        profile = Profile.objects.get(user__username='physician')
        actual = profile.is_staff
        self.assertFalse(actual)

    def test_profile_property_is_patient__when_user_register_as_physician__expect_is_patient_is_false(self):
        profile = Profile.objects.get(user__username='physician')
        actual = profile.is_patient
        self.assertFalse(actual)

    def test_profile_property_is_physician__when_user_register_as_physician__expect_is_physician_is_true(self):
        profile = Profile.objects.get(user__username='physician')
        actual = profile.is_physician
        self.assertTrue(actual)

    def test_profile_str__when_user_register_as_physician__expect_correct_str_method_result(self):
        profile = Profile.objects.get(user__username='physician')
        expected = f'Physician Name: {profile.full_name}, Health Facility: {profile.health_facility.name}, City: {profile.health_facility.city}'
        actual = profile.__str__()
        self.assertEqual(expected, actual)

    def test_profile_str__when_user_register_as_patient__expect_correct_str_method_result(self):
        profile = Profile.objects.get(user__username='patient')
        expected = profile.full_name
        actual = profile.__str__()
        self.assertEqual(expected, actual)

    def test_profile_str__when_user_register_as_staff__expect_correct_str_method_result(self):
        profile = Profile.objects.get(user__username='staff')
        expected = f'Staff Name: {profile.full_name}'
        actual = profile.__str__()
        self.assertEqual(expected, actual)

    def test_profile_property_full_name__when_middle_name_empty__expect_correct_full_name(self):
        profile = Profile.objects.get(user__username='staff')
        profile.middle_name = None
        expected = f'{profile.first_name} {profile.last_name}'
        actual = profile.full_name
        self.assertEqual(expected, actual)

    def test_profile_property_full_name__when_middle_name_not_empty__expect_correct_full_name(self):
        profile = Profile.objects.get(user__username='staff')
        expected = f'{profile.first_name} {profile.middle_name} {profile.last_name}'
        actual = profile.full_name
        self.assertEqual(expected, actual)

    def test_profile_first_name_validator__when_first_name_contains_only_letters__expect_correctly_set_first_name(self):
        profile = Profile.objects.get(user__username='staff')
        profile.first_name = self.CORRECT_NAME
        profile.full_clean()
        profile.save()
        expected = self.CORRECT_NAME
        actual = profile.first_name
        self.assertEqual(expected, actual)

    def test_profile_first_name_validator__when_first_name_contains_number__expect_validation_error(self):
        profile = Profile.objects.get(user__username='staff')
        profile.first_name = self.NAME_CONTAINING_NUMBER
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_profile_first_name_validator__when_first_name_contains_underscore__expect_validation_error(self):
        profile = Profile.objects.get(user__username='staff')
        profile.first_name = self.NAME_CONTAINING_UNDERSCORE
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_profile_first_name_validator__when_first_name_contains_space__expect_validation_error(self):
        profile = Profile.objects.get(user__username='staff')
        profile.first_name = self.NAME_CONTAINING_SPACE
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_profile_first_name_validator__when_first_name_contains_dash__expect_validation_error(self):
        profile = Profile.objects.get(user__username='staff')
        profile.first_name = self.NAME_CONTAINING_DASH
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_profile_middle_name_validator__when_middle_name_contains_only_letters__expect_correctly_set_middle_name(self):
        profile = Profile.objects.get(user__username='staff')
        profile.middle_name = self.CORRECT_NAME
        profile.full_clean()
        profile.save()
        expected = self.CORRECT_NAME
        actual = profile.middle_name
        self.assertEqual(expected, actual)

    def test_profile_middle_name_can_be_empty__when_middle_name_empty__expect_correctly_set_middle_name(self):
        TEST_MIDDLE_NAME = ''
        profile = Profile.objects.get(user__username='staff')
        profile.middle_name = TEST_MIDDLE_NAME
        profile.full_clean()
        profile.save()
        expected = TEST_MIDDLE_NAME
        actual = profile.middle_name
        self.assertEqual(expected, actual)

    def test_profile_middle_name_can_be_none__when_middle_name_none__expect_correctly_set_middle_name(self):
        TEST_MIDDLE_NAME = None
        profile = Profile.objects.get(user__username='staff')
        profile.middle_name = TEST_MIDDLE_NAME
        profile.full_clean()
        profile.save()
        expected = TEST_MIDDLE_NAME
        actual = profile.middle_name
        self.assertEqual(expected, actual)

    def test_profile_middle_name_validator__when_middle_name_contains_number__expect_validation_error(self):
        profile = Profile.objects.get(user__username='staff')
        profile.middle_name = self.NAME_CONTAINING_NUMBER
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_profile_middle_name_validator__when_middle_name_contains_underscore__expect_validation_error(self):
        profile = Profile.objects.get(user__username='staff')
        profile.middle_name = self.NAME_CONTAINING_UNDERSCORE
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_profile_middle_name_validator__when_middle_name_contains_space__expect_validation_error(self):
        profile = Profile.objects.get(user__username='staff')
        profile.middle_name = self.NAME_CONTAINING_SPACE
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_profile_middle_name_validator__when_middle_name_contains_dash__expect_validation_error(self):
        profile = Profile.objects.get(user__username='staff')
        profile.middle_name = self.NAME_CONTAINING_DASH
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_profile_last_name_validator__when_last_name_contains_only_letters__expect_correctly_set_first_name(self):
        profile = Profile.objects.get(user__username='staff')
        profile.last_name = self.CORRECT_NAME
        profile.full_clean()
        profile.save()
        expected = self.CORRECT_NAME
        actual = profile.last_name
        self.assertEqual(expected, actual)

    def test_profile_last_name_validator__when_last_name_contains_number__expect_validation_error(self):
        profile = Profile.objects.get(user__username='staff')
        profile.last_name = self.NAME_CONTAINING_NUMBER
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_profile_last_name_validator__when_last_name_contains_underscore__expect_validation_error(self):
        profile = Profile.objects.get(user__username='staff')
        profile.last_name = self.NAME_CONTAINING_UNDERSCORE
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_profile_last_name_validator__when_last_name_contains_space__expect_validation_error(self):
        profile = Profile.objects.get(user__username='staff')
        profile.last_name = self.NAME_CONTAINING_SPACE
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_profile_last_name_validator__when_last_name_contains_dash__expect_validation_error(self):
        profile = Profile.objects.get(user__username='staff')
        profile.last_name = self.NAME_CONTAINING_DASH
        with self.assertRaises(ValidationError):
            profile.full_clean()
