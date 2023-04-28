from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model."""

    class Roles(models.TextChoices):
        """Roles for custom User model."""

        ADMIN = 'admin'
        USER = 'user'

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='First_name'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Last_name'
    )
    role = models.CharField(
        max_length=5,
        choices=Roles.choices,
        default=Roles.USER,
        verbose_name='Role'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN or self.is_superuser


class Follow(models.Model):
    """Model for following recipe authors."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Author'
    )

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=models.Q(user=models.F('user')),
                name='self_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.author}'
