from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Tag model."""

    name = models.CharField(max_length=200, verbose_name='Name', unique=True)
    color = models.CharField(max_length=7, verbose_name='Color', unique=True)
    slug = models.SlugField(max_length=200, verbose_name='Slug', unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient model."""

    name = models.CharField(max_length=200, verbose_name='Name')
    measurement_unit = models.CharField(max_length=200, verbose_name='Unit')

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe model."""

    name = models.CharField(max_length=200, verbose_name='Name', unique=True)
    text = models.TextField(verbose_name='Text')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='specify a time of at least 1 minute')
        ],
        verbose_name='Cooking time'
    )
    image = models.ImageField(
        upload_to='media/images/',
        verbose_name='Image'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Tags'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ingredients'
    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_recipe'
            )
        ]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Many-to-many model for Recipe and Ingredient instances."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount',
        verbose_name='Recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount',
        verbose_name='Ingredient'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'specify the weight of at least 1 unit')
        ],
        verbose_name='Amount'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe_id} {self.ingredient_id}'


class Favorite(models.Model):
    """Model for favorite recipes."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='User'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Recipe'
    )

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe}_by_{self.user}'


class Cart(models.Model):
    """Model for shopping cart."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='User'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Recipe'
    )

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_cart_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe}_by_{self.user}'
