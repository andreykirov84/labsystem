from django.test import TestCase
from labsystem.laboratory.models import Position


class PositionTestCase(TestCase):
    def setUp(self):
        Position.objects.create(
            name='CTO',
        )

    def test_position_str__when_valid_fields__expect_correct_str_method_result(self):
        position = Position.objects.get(name='CTO')
        expected = position.name
        actual = position.__str__()
        self.assertEqual(expected, actual)
