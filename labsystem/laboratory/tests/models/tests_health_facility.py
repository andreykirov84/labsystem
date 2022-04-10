from django.test import TestCase
from labsystem.laboratory.models import Country, City, HealthFacility


class HealthFacilityTestCase(TestCase):
    def setUp(self):
        country = Country.objects.create(name='Bulgaria', code='BG')
        city = City.objects.create(
            name='Sofia',
            post_code=1000,
            municipality='Sofia',
            province='Sofia',
            country=country,
        )
        HealthFacility.objects.create(
            name='Name',
            address='Address',
            city=city,
            vat='BG11111',
            contact_person='John Doe',
            telephone_number='+359111',
            email='hf_contact@mail.bg',
            comments='Comments',
        )

    def test_health_facility_str__when_valid_fields__expect_correct_str_method_result(self):
        hf = HealthFacility.objects.get(name='Name')
        expected = f'{hf.name} in {hf.city}'
        actual = hf.__str__()
        self.assertEqual(expected, actual)
