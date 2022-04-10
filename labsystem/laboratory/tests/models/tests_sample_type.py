from django.test import TestCase
from labsystem.laboratory.models import SampleType


class SampleTypeTestCase(TestCase):
    NAME = 'blood'

    def setUp(self):
        SampleType.objects.create(
            name=self.NAME,
        )

    def test_sample_type_str__when_valid_fields__expect_correct_str_method_result(self):
        st = SampleType.objects.get(name=self.NAME)
        expected = st.name
        actual = st.__str__()
        self.assertEqual(expected, actual)
