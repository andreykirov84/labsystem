import uuid
import hashlib

"""
Author: Andres Torres
Source: https://www.pythoncentral.io/hashing-strings-with-python/
"""


def hash_string(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_hashed_string(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

