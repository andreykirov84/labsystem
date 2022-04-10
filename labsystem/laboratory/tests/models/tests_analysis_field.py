from django.core.exceptions import ValidationError
from django.test import TestCase
from labsystem.laboratory.models import AnalysisField


class AnalysisFieldTestCase(TestCase):
    NAME = 'blood'
    UNIT = 'IU/l'
    VALUE = 1
    COMMENT = 'Comment'

    def setUp(self):
        AnalysisField.objects.create(
            name=self.NAME,
            unit=self.UNIT,
            male_min=self.VALUE,
            male_max=self.VALUE,
            female_min=self.VALUE,
            female_max=self.VALUE,
            comment=self.COMMENT,
        )

    def test_analysis_field_str__when_valid_fields__expect_correct_str_method_result(self):
        st = AnalysisField.objects.get(name=self.NAME)
        expected = st.name
        actual = st.__str__()
        self.assertEqual(expected, actual)

    def test_analysis_field_male_min_validator__when_value_positive__expect_correctly_set_field(self):
        TEST_VALUE = 100
        af = AnalysisField.objects.get(name=self.NAME)
        af.male_min = TEST_VALUE
        af.full_clean()
        af.save()
        expected = TEST_VALUE
        actual = af.male_min
        self.assertEqual(expected, actual)

    def test_analysis_field_male_min_validator__when_value_is_zero__expect_correctly_set_field(self):
        TEST_VALUE = 0
        af = AnalysisField.objects.get(name=self.NAME)
        af.male_min = TEST_VALUE
        af.full_clean()
        af.save()
        expected = TEST_VALUE
        actual = af.male_min
        self.assertEqual(expected, actual)

    def test_analysis_field_male_min_validator__when_value_is_negative__expect_validation_error(self):
        TEST_VALUE = -100
        af = AnalysisField.objects.get(name=self.NAME)
        af.male_min = TEST_VALUE
        with self.assertRaises(ValidationError):
            af.full_clean()

    def test_analysis_field_male_max_validator__when_value_positive__expect_correctly_set_field(self):
        TEST_VALUE = 100
        af = AnalysisField.objects.get(name=self.NAME)
        af.male_max = TEST_VALUE
        af.full_clean()
        af.save()
        expected = TEST_VALUE
        actual = af.male_max
        self.assertEqual(expected, actual)

    def test_analysis_field_male_max_validator__when_value_is_zero__expect_correctly_set_field(self):
        TEST_VALUE = 0
        af = AnalysisField.objects.get(name=self.NAME)
        af.male_max = TEST_VALUE
        af.full_clean()
        af.save()
        expected = TEST_VALUE
        actual = af.male_max
        self.assertEqual(expected, actual)

    def test_analysis_field_male_max_validator__when_value_is_negative__expect_validation_error(self):
        TEST_VALUE = -100
        af = AnalysisField.objects.get(name=self.NAME)
        af.male_max = TEST_VALUE
        with self.assertRaises(ValidationError):
            af.full_clean()

    def test_analysis_field_female_min_validator__when_value_positive__expect_correctly_set_field(self):
        TEST_VALUE = 100
        af = AnalysisField.objects.get(name=self.NAME)
        af.female_min = TEST_VALUE
        af.full_clean()
        af.save()
        expected = TEST_VALUE
        actual = af.female_min
        self.assertEqual(expected, actual)

    def test_analysis_field_female_min_validator__when_value_is_zero__expect_correctly_set_field(self):
        TEST_VALUE = 0
        af = AnalysisField.objects.get(name=self.NAME)
        af.female_min = TEST_VALUE
        af.full_clean()
        af.save()
        expected = TEST_VALUE
        actual = af.female_min
        self.assertEqual(expected, actual)

    def test_analysis_field_female_min_validator__when_value_is_negative__expect_validation_error(self):
        TEST_VALUE = -100
        af = AnalysisField.objects.get(name=self.NAME)
        af.female_min = TEST_VALUE
        with self.assertRaises(ValidationError):
            af.full_clean()

    def test_analysis_field_female_max_validator__when_value_positive__expect_correctly_set_field(self):
        TEST_VALUE = 100
        af = AnalysisField.objects.get(name=self.NAME)
        af.female_max = TEST_VALUE
        af.full_clean()
        af.save()
        expected = TEST_VALUE
        actual = af.female_max
        self.assertEqual(expected, actual)

    def test_analysis_field_female_max_validator__when_value_is_zero__expect_correctly_set_field(self):
        TEST_VALUE = 0
        af = AnalysisField.objects.get(name=self.NAME)
        af.female_max = TEST_VALUE
        af.full_clean()
        af.save()
        expected = TEST_VALUE
        actual = af.female_max
        self.assertEqual(expected, actual)

    def test_analysis_field_female_max_validator__when_value_is_negative__expect_validation_error(self):
        TEST_VALUE = -100
        af = AnalysisField.objects.get(name=self.NAME)
        af.female_max = TEST_VALUE
        with self.assertRaises(ValidationError):
            af.full_clean()
