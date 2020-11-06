from django.contrib import admin

from .models import Recipe, Ingredient, IngredientIncomposition, Tags


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name','description','slug')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name','units_of_measurement')

@admin.register(IngredientIncomposition)
class IngredientIncompositionAdmin(admin.ModelAdmin):
    list_display = ('quantity',)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_dispaly = ('name', 'slug')