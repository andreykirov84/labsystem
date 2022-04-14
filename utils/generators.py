from django.utils.crypto import get_random_string
import string as py_string


def get_secure_random_string(length):
    lower = py_string.ascii_lowercase
    upper = py_string.ascii_uppercase
    num = py_string.digits

    allowed_chars = lower + upper + num

    password = get_random_string(
        length=length,
        allowed_chars=allowed_chars
    )

    return ''.join(password)
