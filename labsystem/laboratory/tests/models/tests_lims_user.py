from django.test import TestCase
from django.utils import timezone

from labsystem.auth_app.models import LimsUser


class LimsUserTestCase(TestCase):
    def setUp(self):
        test_user = LimsUser.objects.create(username="test_user", password=111)

    def test_lims_user_soft_delete__when_user_soft_deleted__expect_deleted_at_field_set_to_timezone_now(self):
        user = LimsUser.objects.get(username='test_user')
        user.soft_delete()
        self.assertAlmostEqual(
            user.deleted_at,
            timezone.now(),
            delta=timezone.timedelta(seconds=1))

    def test_lims_user_restore__when_user_soft_deleted_and_restored__expect_deleted_at_set_to_none(self):
        user = LimsUser.objects.get(username='test_user')
        user.soft_delete()
        user.restore()
        expected = None
        actual = user.deleted_at
        self.assertEqual(expected, actual)

    def test_lims_user_hard_delete__when_user_exist__expect_user_deleted(self):
        user = LimsUser.objects.get(username='test_user')
        user.hard_delete()
        actual = LimsUser.objects.filter(username='test_user').exists()
        self.assertFalse(actual)


