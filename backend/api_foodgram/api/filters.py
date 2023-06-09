from django_filters import rest_framework as filters
from django_filters.widgets import BooleanWidget

from recipes.models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    """A filter for Recipe instances."""

    author = filters.CharFilter(field_name='author__id')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='get_favorites',
        widget=BooleanWidget()
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_carts',
        widget=BooleanWidget()
    )

    def get_favorites(self, queryset, field_name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def get_carts(self, queryset, field_name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
