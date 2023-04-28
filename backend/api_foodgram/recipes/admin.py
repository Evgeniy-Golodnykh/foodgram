from django.contrib import admin

from .models import Cart, Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class IngredientInline(admin.StackedInline):
    """Add RecipeIngredient instances to Recipe admin panel."""

    model = RecipeIngredient
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    """Custom Ingredient admin panel."""

    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    """Custom Recipe admin panel."""

    inlines = (IngredientInline,)
    list_display = ('name', 'author', 'favorites_count')
    list_filter = ('name', 'author', 'tags')

    def favorites_count(self, obj):
        return obj.favorite.count()


admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
