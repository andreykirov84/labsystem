from django.test import TestCase
from labsystem.laboratory.models import Sex


class SexTestCase(TestCase):
    def setUp(self):
        Sex.objects.create(
            name='Male',
        )

    def test_sex_str__when_valid_fields__expect_correct_str_method_result(self):
        sex = Sex.objects.get(name='Male')
        expected = sex.name
        actual = sex.__str__()
        self.assertEqual(expected, actual)
