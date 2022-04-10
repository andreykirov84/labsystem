from django.test import TestCase
from labsystem.laboratory.models import Specialty


class SpecialtyTestCase(TestCase):
    def setUp(self):
        Specialty.objects.create(
            name='Cardiology',
        )

    def test_speciality_str__when_valid_fields__expect_correct_str_method_result(self):
        speciality = Specialty.objects.get(name='Cardiology')
        expected = speciality.name
        actual = speciality.__str__()
        self.assertEqual(expected, actual)
