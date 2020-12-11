from django.contrib import admin

from .models import Recipes, Ingredient, IngredientIncomposition, Tags


@admin.register(Recipes)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name','description',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name','units_of_measurement')

@admin.register(IngredientIncomposition)
class IngredientIncompositionAdmin(admin.ModelAdmin):
    list_display = ('recipe','quantity','ingredient')


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_dispaly = ('name', 'slug')


from django.contrib import admin
from .models import Favorites,Follow,ShoppingList

@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'fuser', )
    search_fields = ('fuser', )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', )
    search_fields = ('user', )

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe',)