from django.test import TestCase
from labsystem.laboratory.models import Department


class DepartmentTestCase(TestCase):
    NAME = 'NAME'
    DESCRIPTION = 'Description'
    TEL_NUMBER = '+359888'
    EMAIL = 'mail@mail.bg'

    def setUp(self):
        Department.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
            telephone_number=self.TEL_NUMBER,
            email=self.EMAIL
        )

    def test_department_str__when_valid_fields__expect_correct_str_method_result(self):
        department = Department.objects.get(name=self.NAME)
        expected = department.name
        actual = department.__str__()
        self.assertEqual(expected, actual)
