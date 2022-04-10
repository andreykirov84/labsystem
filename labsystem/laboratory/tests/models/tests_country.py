from django.test import TestCase
from labsystem.laboratory.models import Country


class CountryTestCase(TestCase):
    def setUp(self):
        Country.objects.create(name='Bulgaria', code='BG')

    def test_country_str__when_valid_fields__expect_correct_str_method_result(self):
        country = Country.objects.get(name='Bulgaria')
        expected = country.name
        actual = country.__str__()
        self.assertEqual(expected, actual)
