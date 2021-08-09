from django.core.paginator import Paginator
from django.db.models import Sum

from .models import IngredientRecipe, Tag


def paginate_page(request, recipe_list):
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page


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
    else:
        for tag in Tag.objects.all():
            tags.add(tag.pk)
    return tags
