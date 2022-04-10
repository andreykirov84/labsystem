from django.core.exceptions import ValidationError
from django.test import TestCase
from labsystem.laboratory.models import Analysis


class AnalysisTestCase(TestCase):
    NAME = 'Name'
    VALUE = 1
    COMMENT = 'Comment'
    DESCRIPTION = 'Description'
    CURRENCY = 'EUR'
    PRICE = 1
    TAT = 1

    def setUp(self):
        Analysis.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
            currency=self.CURRENCY,
            price=self.PRICE,
            tat=self.TAT,
        )

    def test_analysis_str__when_valid_fields__expect_correct_str_method_result(self):
        a = Analysis.objects.get(name=self.NAME)
        expected = f'{a.name}, price: {a.price} {a.currency}'
        actual = a.__str__()
        self.assertEqual(expected, actual)

    def test_analysis_price_validator__when_value_positive__expect_correctly_set_field(self):
        TEST_VALUE = 100
        a = Analysis.objects.get(name=self.NAME)
        a.price = TEST_VALUE
        a.full_clean()
        a.save()
        expected = TEST_VALUE
        actual = a.price
        self.assertEqual(expected, actual)

    def test_analysis_price_validator__when_value_is_zero__expect_correctly_set_field(self):
        TEST_VALUE = 0
        a = Analysis.objects.get(name=self.NAME)
        a.price = TEST_VALUE
        a.full_clean()
        a.save()
        expected = TEST_VALUE
        actual = a.price
        self.assertEqual(expected, actual)

    def test_analysis_price_validator__when_value_is_negative__expect_validation_error(self):
        TEST_VALUE = -1
        a = Analysis.objects.get(name=self.NAME)
        a.price = TEST_VALUE
        with self.assertRaises(ValidationError):
            a.full_clean()

    def test_analysis_tat_validator__when_value_positive__expect_correctly_set_field(self):
        TEST_VALUE = 100
        a = Analysis.objects.get(name=self.NAME)
        a.tat = TEST_VALUE
        a.full_clean()
        a.save()
        expected = TEST_VALUE
        actual = a.tat
        self.assertEqual(expected, actual)

    def test_analysis_tat_validator__when_value_is_zero__expect_correctly_set_field(self):
        TEST_VALUE = 0
        a = Analysis.objects.get(name=self.NAME)
        a.tat = TEST_VALUE
        a.full_clean()
        a.save()
        expected = TEST_VALUE
        actual = a.tat
        self.assertEqual(expected, actual)

    def test_analysis_tat_validator__when_value_is_negative__expect_validation_error(self):
        TEST_VALUE = -1
        a = Analysis.objects.get(name=self.NAME)
        a.tat = TEST_VALUE
        with self.assertRaises(ValidationError):
            a.full_clean()
