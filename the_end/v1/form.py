from django import forms
from django.forms import ModelForm

from .models import Recipe


class RecipeCreateForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'tags', "time", "description", "image",)
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if len(name) < 1:
            raise forms.ValidationError(
                f'Введите название!')
        return name


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', "time", "description", "image",)