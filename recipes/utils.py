from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from .models import (Ingredient, IngredientRecipe)


def paginate_page(request, recipe_list):
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page

def get_ingredients(request):
    ingredients = {}
    post = request.POST
    for key, name in post.items():
        if key.startswith('nameIngredient'):
            num = key.partition('_')[-1]
            ingredients[name] = post[f'valueIngredient_{num}']
    return ingredients


def save_recipe(request, form):
    with transaction.atomic():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()

        objs = []
        ingredients = get_ingredients(request)

        for name, quantity in ingredients.items():
            ingredient = get_object_or_404(Ingredient, name=name)

            objs.append(
                IngredientRecipe(
                    recipe=recipe,
                    ingredient=ingredient,
                    value=quantity
                )
            )
        IngredientRecipe.objects.bulk_create(objs)
        form.save_m2m()
        return recipe


def union_ingredients(request):
    combined_ingredients = {}
    items = IngredientRecipe.objects.filter(
        recipe__listed_recipes__user=request.user
    ).values(
        'ingredient__name',
        'ingredient__units'
    ).annotate(
        amount=Sum('value')
    ).all()

    for item in items:
        ingredient_name = f"{item['ingredient__name']}, {item['ingredient__units']}"
        combined_ingredients[ingredient_name] = item['amount']

    return combined_ingredients


def tags_stuff(request, recipe_list):
    tags = used_tags(request)
    if tags:
        recipe_list = recipe_list.filter(tags__id__in=tags).distinct()
    return recipe_list


def used_tags(request):
    tags = set()
    if 'tag' in request.GET:
        tags = set(map(int, request.GET.getlist('tag')))
    return tags
