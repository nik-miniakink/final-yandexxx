from django import forms
from django.forms import ModelForm

from .models import Recipes

class RecipeForm(ModelForm):
    class Meta:
        model = Recipes
        fields = ('name', "time", "description", "image",)


