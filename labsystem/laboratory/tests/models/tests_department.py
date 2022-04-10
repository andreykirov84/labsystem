from django.test import TestCase
from labsystem.laboratory.models import Department


class DepartmentTestCase(TestCase):
    def setUp(self):
        Department.objects.create(
            name='IT',
            description='IT',
            telephone_number='+359555555',
            email='department@mail.bg'
        )

    def test_department_str__when_valid_fields__expect_correct_str_method_result(self):
        department = Department.objects.get(name='IT')
        expected = department.name
        actual = department.__str__()
        self.assertEqual(expected, actual)
