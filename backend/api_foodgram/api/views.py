from django.db import models
from django.http import HttpResponse
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RecipeFilter
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (
    CreateUpdateRecipeSerializer, FavoriteOrCartRecipeSerializer,
    IngredientSerializer, RecipeSerializer, TagSerializer,
)
from .tools import create_instance, destroy_instance
from recipes.models import (
    Cart, Favorite, Ingredient, Recipe, RecipeIngredient, Tag,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """A viewset for viewing Tag instances."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """A viewset for viewing Ingredient instances."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing Recipe instances."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CreateUpdateRecipeSerializer
        return RecipeSerializer

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return create_instance(
                Recipe, Favorite, FavoriteOrCartRecipeSerializer, request, pk
            )
        return destroy_instance(Recipe, Favorite, request, pk)

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return create_instance(
                Recipe, Cart, FavoriteOrCartRecipeSerializer, request, pk
            )
        return destroy_instance(Recipe, Cart, request, pk)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        if not request.user.cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = RecipeIngredient.objects.filter(
            recipe__cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=models.Sum('amount')).order_by('ingredient__name')
        cart = (
            f'{request.user.get_full_name()} shopping list includes:\n'
        )
        cart += '\n'.join([
            f'- {ingredient["ingredient__name"]} / '
            f'{ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}'
            for ingredient in ingredients
        ])
        filename = 'Shopping_list.txt'
        response = HttpResponse(cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
