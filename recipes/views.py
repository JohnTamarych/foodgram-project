from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from django.core.paginator import Paginator

from .forms import RecipeForm
from .models import Recipe, Tag

def recipe(request):
    form = RecipeForm(request.POST or None)

    return render(
        request, 
        'recipes/form_recipe.html', 
        {'form': form, }
    )


def index(request):
    recipe_list = Recipe.objects.all()
    # recipe_list = tags_stuff(request, recipe_list)

    paginator = Paginator(recipe_list, 6)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request,
                  'recipes/index.html',
                  {
                      'page': page,
                      'paginator': paginator,
                      'all_tags': Tag.objects.all(),
                    #   'tags': used_tags(request),
                  }
                  )

def single_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    return render(
        request,
        'recipes/single_page.html',
        {
            'recipe': recipe,
        }
    )
