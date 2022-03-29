from django.contrib.auth import models as auth_models
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from labsystem.auth_app.managers import LimsUserManager, SoftDeleteManager
from utils.abstract_models import SoftDeleteModel


class LimsUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LENGTH = 25
    USERNAME_MIN_LENGTH = 6

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(USERNAME_MIN_LENGTH),
        ),
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_physician = models.BooleanField(
        default=False,
    )

    is_patient = models.BooleanField(
        default=False,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    deleted_at = models.DateTimeField(null=True, default=None)

    USERNAME_FIELD = 'username'

    objects = LimsUserManager()
    undeleted_objects = SoftDeleteManager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
