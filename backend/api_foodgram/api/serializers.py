from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Cart, Favorite, Ingredient, Recipe, RecipeIngredient, Tag,
)
from users.serializers import CustomUserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """A serializer to read Tag instances."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """A serializer to read Ingredient instances."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """A serializer to read Ingredient instances for Recipe views."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
    """A serializer to add IngredientRecipe instances."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects)
    amount = serializers.IntegerField(min_value=1, write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """A serializer to read Recipe instances."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        return RecipeIngredientSerializer(
            RecipeIngredient.objects.filter(recipe=obj),
            many=True,
        ).data

    def get_is_favorited(self, obj):
        request = self.context.get('request', False)
        return request and Favorite.cart_set.filter(user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request', False)
        return request and Cart.cart_set.filter(user=request.user).exists()


class CreateUpdateRecipeSerializer(serializers.ModelSerializer):
    """A serializer to create/update Recipe instances."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects,
        many=True
    )
    ingredients = AddIngredientToRecipeSerializer(many=True)
    image = Base64ImageField(use_url=True, max_length=None)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        validated_data['author'] = self.context['request'].user
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        objs = [RecipeIngredient(
            recipe=recipe,
            ingredient=get_object_or_404(Ingredient, id=data['id'].id),
            amount=data['amount']
        ) for data in ingredients]

        RecipeIngredient.objects.bulk_create(objs=objs)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = get_object_or_404(Recipe, id=instance.id)
        recipe.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        for data in ingredients:
            ingredient = get_object_or_404(Ingredient, id=data['id'].id)
            amount = data['amount']
            RecipeIngredient.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount
            )
        return super().update(instance, validated_data)


class FavoriteOrCartRecipeSerializer(serializers.ModelSerializer):
    """A serializer to read favorite or cart recipes."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
