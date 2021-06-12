from django.forms import ModelForm
from django import forms

from .models import Recipe


class RecipeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True

    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'cooking_time', 'description', 'image',)

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
