from django import forms
from django.core.exceptions import BadRequest
from django.db import IntegrityError, transaction
from django.forms import ModelForm

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
                float_val = float(ingredient_value.replace(',', '.'))
                self.ingredients[ingredient_name] = float(float_val)
        for ingredient_title, quantity in self.ingredients.items():
            if not Ingredient.objects.filter(name=ingredient_title).exists():
                msg = 'Добавлен несуществующий ингредиент'
                self.add_error(None, msg)

    def create_recipe_ingredients(self, recipe):
        IngredientRecipe.objects.filter(recipe=recipe).delete()
        for ingredient_title, quantity in self.ingredients.items():
            ingredient = Ingredient.objects.get(name=ingredient_title)
            recipeingredients = IngredientRecipe(recipe=recipe,
                                                 ingredient=ingredient,
                                                 value=quantity)
            recipeingredients.save()

    def clean(self):
        self.get_ingredients()
        cleaned_data = super().clean()
        if not self.ingredients:
            msg = 'Необходимо добавить ингредиенты'
            self.add_error(None, msg)
        return cleaned_data

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                recipe = super().save(commit=False)
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
