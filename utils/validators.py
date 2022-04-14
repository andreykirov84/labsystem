from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            # Invalid case
            raise ValidationError('Value must contain only letters')


def validate_only_digits(value):
    for ch in value:
        if not ch.isdigit():
            # Invalid case
            raise ValidationError('Value must contain only digits')


def validate_value_not_negative(value):
    if value < 0:
        # Invalid case
        raise ValidationError('Value must be equal or larger then 0')


def validate_telephone(value):
    """
    accept only phone numbers in format +35924204242
    """
    error_message = 'value must be in format +35924204242'
    if value[0] != '+':
        # Invalid case
        raise ValidationError(error_message)

    for ch in value[1::]:
        if not ch.isdigit():
            # Invalid case
            raise ValidationError(error_message)


def validate_only_letters_and_spaces(value):
    stripped_value = value.replace(' ', '')
    result = True
    for ch in stripped_value:
        if not ch.isalpha():
            result = False
            break
    return result
