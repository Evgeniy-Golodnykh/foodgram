from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import (
    Cart, Favorite, Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag,
)
from users.models import Follow
from users.serializers import CustomUserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """A serializer for Tag instances."""

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """A serializer for Ingredient instances."""

    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    """A serializer for Recipe instances."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Recipe


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """A serializer for favorite recipes."""

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe
