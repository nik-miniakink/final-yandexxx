from django.contrib import admin

from .models import Recipe, Ingredient, IngredientIncomposition


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name','description','slug')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name','units_of_measurement')

@admin.register(IngredientIncomposition)
class IngredientIncompositionAdmin(admin.ModelAdmin):
    list_display = ('quantity',)