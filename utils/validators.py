from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class MaxFileSizeInMbValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    @staticmethod
    def __megabytes_to_bytes_converter(value):
        return value * 1024 * 1024

    def __get_exception_message(self):
        return f'Max file size is {self.max_size:.2f} MB'

    def __call__(self, value):
        max_size_in_bytes = self.__megabytes_to_bytes_converter(self.max_size)

        if value.file.size > max_size_in_bytes:
            raise ValidationError(self.__get_exception_message())


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


@deconstructible
class MinDateValidator:
    def __init__(self, min_date):
        self.min_date = min_date

    def __call__(self, value):
        if value < self.min_date:
            raise ValidationError(f'Date must be greater than {self.min_date}')


@deconstructible
class MaxDateValidator:
    def __init__(self, max_date):
        self.max_date = max_date

    def __call__(self, value):
        if self.max_date < value:
            raise ValidationError(f'Date must be earlier than {self.max_date}')


def validate_only_letters_and_spaces(value):
    stripped_value = value.replace(' ', '')
    result = True
    for ch in stripped_value:
        if not ch.isalpha():
            result = False
            break
    return result
