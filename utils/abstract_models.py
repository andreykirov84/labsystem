from django.db import models

from labsystem.auth_app.managers import LimsUserManager, SoftDeleteManager


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    objects = LimsUserManager()
    undeleted_objects = SoftDeleteManager()

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True

