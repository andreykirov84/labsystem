from django.test import TestCase
from labsystem.laboratory.models import PidType


class PidTypeTestCase(TestCase):
    def setUp(self):
        PidType.objects.create(
            name='EGN',
        )

    def test_pid_type_str__when_valid_fields__expect_correct_str_method_result(self):
        pid = PidType.objects.get(name='EGN')
        expected = pid.name
        actual = pid.__str__()
        self.assertEqual(expected, actual)
