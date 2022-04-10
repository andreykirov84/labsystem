from django.test import TestCase
from labsystem.laboratory.models import ResultStatus


class ResultStatusTestCase(TestCase):
    def setUp(self):
        ResultStatus.objects.create(
            name='Ready',
        )

    def test_department_str__when_valid_fields__expect_correct_str_method_result(self):
        rs = ResultStatus.objects.get(name='Ready')
        expected = rs.name
        actual = rs.__str__()
        self.assertEqual(expected, actual)
