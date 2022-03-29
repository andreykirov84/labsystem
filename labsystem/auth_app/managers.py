from django.contrib.auth import base_user as auth_base
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class LimsUserManager(auth_base.BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_patient', False)
        extra_fields.setdefault('is_physician', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_patient') is True:
            raise ValueError('Superuser must have is_patient=False.')
        if extra_fields.get('is_physician') is True:
            raise ValueError('Superuser must have is_physician=False.')

        return self._create_user(username, password, **extra_fields)

    def create_patient_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_patient', True)
        extra_fields.setdefault('is_physician', False)

        if extra_fields.get('is_staff') is True:
            raise ValueError('Patient must have is_staff=False.')
        if extra_fields.get('is_superuser') is True:
            raise ValueError('Patient must have is_superuser=False.')
        if extra_fields.get('is_patient') is not True:
            raise ValueError('Patient must have is_patient=True.')
        if extra_fields.get('is_physician') is True:
            raise ValueError('Patient must have is_physician=False.')

        return self._create_user(username, password, **extra_fields)

    def create_physician_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_patient', False)
        extra_fields.setdefault('is_physician', True)

        if extra_fields.get('is_staff') is True:
            raise ValueError('Physician must have is_staff=False.')
        if extra_fields.get('is_superuser') is True:
            raise ValueError('Physician must have is_superuser=False.')
        if extra_fields.get('is_patient') is True:
            raise ValueError('Physician must not have is_patient=False.')
        if extra_fields.get('is_physician') is not True:
            raise ValueError('Physician must not have is_physician=True.')

        return self._create_user(username, password, **extra_fields)

    def create_staff_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_patient', True)
        extra_fields.setdefault('is_physician', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True.')
        if extra_fields.get('is_superuser') is True:
            raise ValueError('Staff must have is_superuser=False.')
        if extra_fields.get('is_patient') is not True:
            raise ValueError('Staff must have is_patient=True.')
        if extra_fields.get('is_physician') is True:
            raise ValueError('Staff must have is_physician=False.')

        return self._create_user(username, password, **extra_fields)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()


class SoftDeleteManager(auth_base.BaseUserManager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
