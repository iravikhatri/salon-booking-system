from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):

    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    is_member = models.BooleanField(default=False, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name_plural = 'Users'


    def __str__(self):
        return self.email


    def full_name(self):
        return f'{self.first_name} {self.last_name}'
