from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Roles(models.TextChoices):

        USER = 'user'
        ADMIN = 'admin'

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='email',
    )
    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        default=Roles.USER,
        verbose_name='role',
    )

    class Meta:
        ordering = ['username']

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN or self.is_superuser
