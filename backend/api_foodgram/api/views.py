from rest_framework import filters, mixins, permissions, viewsets

from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (
    CreateUpdateRecipeSerializer, IngredientSerializer, RecipeSerializer,
    TagSerializer,
)
from recipes.models import Ingredient, Recipe, Tag


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """Create+Destroy+list mix ViewSet."""


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

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CreateUpdateRecipeSerializer
        return RecipeSerializer
