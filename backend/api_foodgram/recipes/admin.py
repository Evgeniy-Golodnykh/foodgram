from django.contrib import admin

from .models import (
    Cart, Favorite, Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag,
)

admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
admin.site.register(Tag)
