from django.core.exceptions import ValidationError
from django.test import TestCase

from utils.validators import validate_only_letters, validate_only_digits, validate_telephone


class ValidatorsTests(TestCase):
    ONLY_LETTERS = 'abC'
    MIX_LETTERS_AND_DIGITS = 'abC2'
    ONLY_DIGITS = '123'
    VALID_TELEPHONE = '+359'
    INVALID_TELEPHONE = '359'

    def test_validate_only_letters_validator_when_all_letters__expect_do_nothing(self):
        validate_only_letters(self.ONLY_LETTERS)
        self.assertTrue(True)

    def test_validate_only_letters_validator__when_contains_non_letter__should_raise(self):
        with self.assertRaises(ValidationError) as context:
            validate_only_letters(self.MIX_LETTERS_AND_DIGITS)
        self.assertIsNotNone(context.exception)

    def test_validate_only_digits_validator__when_all_digits__expect_do_nothing(self):
        validate_only_digits(self.ONLY_DIGITS)
        self.assertTrue(True)

    def test_validate_only_digits_validator__when_contains_non_digits__should_raise(self):
        with self.assertRaises(ValidationError) as context:
            validate_only_digits(self.MIX_LETTERS_AND_DIGITS)
        self.assertIsNotNone(context.exception)

    def test_validate_telephone_validator__when_correct_value__expect_do_nothing(self):
        validate_telephone(self.VALID_TELEPHONE)
        self.assertTrue(True)

    def test_validate_telephone_validator__when_invalid_value__should_raise(self):
        with self.assertRaises(ValidationError) as context:
            validate_telephone(self.INVALID_TELEPHONE)
        self.assertIsNotNone(context.exception)

