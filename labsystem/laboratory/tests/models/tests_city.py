from django.test import TestCase
from labsystem.laboratory.models import Country, City


class CityTestCase(TestCase):
    def setUp(self):
        country = Country.objects.create(name='Bulgaria', code='BG')
        City.objects.create(
            name='Sofia',
            post_code=1000,
            municipality='Sofia',
            province='Sofia',
            country=country,
        )

    def test_city_str__when_valid_fields__expect_correct_str_method_result(self):
        city = City.objects.get(name='Sofia')
        expected = f'{city.name}, province: {city.province}'
        actual = city.__str__()
        self.assertEqual(expected, actual)
