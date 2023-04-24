from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag
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
    """A serializer for read Recipe instances."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Recipe


class CreateUpdateRecipeSerializer(serializers.ModelSerializer):
    """A serializer for create/update Recipe instances."""

    tags = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Tag.objects,
        many=True
    )
    ingredients = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Ingredient.objects,
        many=True
    )
    author = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = (
            'author', 'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time'
        )
        model = Recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data


class CurrentRecipeDefault:
    """A function to receive recipe id from path parameter."""

    requires_context = True

    def __call__(self, serializer_field):
        context = serializer_field.context['request'].parser_context
        return get_object_or_404(
            Recipe, id=context.get('kwargs').get('recipe_id'))


class FavoriteOrCartRecipeSerializer(serializers.ModelSerializer):
    """A serializer for read favorite or cart recipes."""

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class CreateDestroyFavoriteRecipeSerializer(serializers.ModelSerializer):
    """A serializer for create/update Favorite instances."""

    author = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    recipe = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
        default=CurrentRecipeDefault()
    )

    class Meta:
        fields = '__all__'
        model = Favorite


class CreateDestroyCartRecipeSerializer(serializers.ModelSerializer):
    """A serializer for create/update Cart instances."""

    author = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    recipe = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
        default=CurrentRecipeDefault()
    )

    class Meta:
        fields = '__all__'
        model = Cart
