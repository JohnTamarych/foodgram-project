from django import forms
from django.core.exceptions import BadRequest, ValidationError
from django.db import IntegrityError, transaction
from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from .models import Ingredient, IngredientRecipe, Recipe


class RecipeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.ingredients = {}
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True

    def get_ingredients(self):
        for key, ingredient_name in self.data.items():
            if key.startswith('nameIngredient'):
                ingredient_value = self.data['valueIngredient' + key[14:]]
                self.ingredients[ingredient_name] = float(ingredient_value)

    def create_recipe_ingredients(self, recipe):
        for ingredient_title, quantity in self.ingredients.items():
            ingredient = get_object_or_404(Ingredient,
                                           name=ingredient_title)
            recipeingredients = IngredientRecipe(recipe=recipe,
                                                 ingredient=ingredient,
                                                 value=quantity)
            recipeingredients.save()

    def clean(self):
        self.get_ingredients()
        cleaned_data = super().clean()
        if not self.ingredients:
            error_message = ValidationError('Ingredients list is empty')
            self.add_error(None, error_message)
        return cleaned_data

    def save(self, *args, **kwargs):
        user = kwargs.get('user')
        try:
            with transaction.atomic():
                recipe = super().save(commit=False)
                recipe.author = user
                recipe.save()
                self.create_recipe_ingredients(recipe)
                self.save_m2m()
        except IntegrityError as save_error:
            raise BadRequest('Error while saving') from save_error
        return recipe

    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'cooking_time', 'description', 'image',)

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
