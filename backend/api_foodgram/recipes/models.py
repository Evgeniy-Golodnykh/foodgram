from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='name')
    color = models.CharField(max_length=7)
    slug = models.SlugField(unique=True, max_length=200, verbose_name='slug')

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='name')
    measurement_unit = models.CharField(max_length=7, verbose_name='unit')
    amount = models.SmallIntegerField(verbose_name='amount')

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'
        ordering = ['name']

    def __str__(self):
        return self.name