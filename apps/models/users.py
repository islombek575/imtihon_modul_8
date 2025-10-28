import re

from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField
from rest_framework.exceptions import ValidationError

from apps.managers import CustomUserManager


class User(AbstractUser):
    phone = CharField(max_length=15, unique=True)
    objects = CustomUserManager()
    username = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def check_phone(self):
        digits = re.findall(r'\d', self.phone)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        self.phone = phone.removeprefix('998')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.check_phone()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)



def __str__(self):
        return self.phone

