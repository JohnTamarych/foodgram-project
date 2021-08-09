import json

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from foodgram.settings import PAGE_SIZE

from .forms import RecipeForm
from .models import Cart, Favorite, Follow, Ingredient, Recipe, Tag, User
from .pdfwork import make_pdf
from .utils import paginate_page, tags_stuff, union_ingredients, used_tags


@login_required
def new_recipe(request):
    recipe_form = RecipeForm(request.POST or None, files=request.FILES or None)
    if recipe_form.is_valid():
        recipe_form.instance.author = request.user
        recipe = recipe_form.save()
        return redirect('index')
    return render(
        request,
        'recipes/form_recipe.html',
        {
            'form': recipe_form,
            'all_tags': Tag.objects.all(),
        },
    )


def index(request):
    recipe_list = Recipe.objects.order_by('-pub_date').all()
    recipe_list = tags_stuff(request, recipe_list)
    page = paginate_page(request, recipe_list)
    page_size = PAGE_SIZE
    return render(
        request,
        'recipes/index.html',
        {
            'page': page,
            'page_size': page_size,
            'all_tags': Tag.objects.all(),
            'tags': used_tags(request),
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


@login_required
def follow_index(request):
    recipe_list = Recipe.objects.order_by('-pub_date').filter(
        author__following__user=request.user
    )

    recipe_list = tags_stuff(request, recipe_list)

    follows = request.user.follower.all()
    user_list = [follow.author for follow in follows]
    page = paginate_page(request, user_list)
    page_size = PAGE_SIZE
    return render(request,
                  'recipes/follow.html',
                  {
                      'page': page,
                      'page_size': page_size,
                      'all_tags': Tag.objects.all(),
                      'tags': used_tags(request),
                  }
                  )


@login_required
def favorite(request):
    recipe_list = Recipe.objects.filter(favorite_recipes__user=request.user)
    recipe_list = tags_stuff(request, recipe_list)
    page = paginate_page(request, recipe_list)
    page_size = PAGE_SIZE
    return render(request,
                  'recipes/favorites.html',
                  {
                      'page': page,
                      'page_size': page_size,
                      'all_tags': Tag.objects.all(),
                      'tags': used_tags(request),
                  }
                  )


def shoplist(request):
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(listed_recipes__user=request.user)
    else:
        if request.session.get('cart') is not None:
            cart = request.session.get('cart')

            recipes = Recipe.objects.filter(id__in=cart)
        else:
            recipes = None

    return render(
        request,
        'recipes/shop_list.html',
        {
            'recipes': recipes,
        }
    )


def ingredients(request):
    name = request.GET['query']
    ingredients = Ingredient.objects.filter(
        name__istartswith=name
    ).values('name', 'units')
    return JsonResponse(
        [
            {
                'title': ingredient['name'],
                'dimension': ingredient['units']
            }
            for ingredient in ingredients
        ],
        safe=False
    )


def author_recipes(request, username):
    author = get_object_or_404(User, username=username)

    recipe_list = author.recipes.all().order_by('-pub_date')

    recipe_list = tags_stuff(request, recipe_list)
    page = paginate_page(request, recipe_list)
    page_size = PAGE_SIZE
    return render(
        request,
        'recipes/author_recipes.html',
        {
            'page': page,
            'page_size': page_size,
            'creator': author,
            'all_tags': Tag.objects.all(),
            'tags': used_tags(request),
        }
    )


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if not request.user.is_staff and recipe.author != request.user:
        return redirect(
            reverse(
                'single',
                kwargs={'id': recipe_id}
            )
        )
    recipe_form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
    if recipe_form.is_valid():
        recipe = recipe_form.save(user=request.user)
        return redirect('index')
    edit = True

    return render(
        request,
        'recipes/form_recipe.html',
        {
            'form': recipe_form,
            'edit': edit,
            'all_tags': Tag.objects.all(),
            'recipe': recipe,
        }
    )


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.author == request.user:
        recipe.delete()
    return redirect(reverse('index'))


@login_required
def profile_follow(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    author_id = int(body['id'])
    author = get_object_or_404(User, id=author_id)
    if not Follow.objects.filter(user=request.user, author=author).exists():
        Follow.objects.create(user=request.user, author=author)
    return JsonResponse({'success': True})


@login_required
def profile_unfollow(request, author_id):
    author = get_object_or_404(User, id=author_id)
    follow = Follow.objects.filter(user=request.user, author=author)
    follow.delete()
    return JsonResponse({'success': False})


@login_required
def add_to_favorites(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    recipe_id = int(body['id'])
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if not Favorite.objects.filter(user=request.user, recipe=recipe).exists():
        Favorite.objects.create(user=request.user, recipe=recipe)
    return JsonResponse({'success': True})


@login_required
def remove_from_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
    favorite.delete()
    return JsonResponse({'success': True})


@login_required
def add_to_list(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    recipe_id = int(body['id'])
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if not Cart.objects.filter(user=request.user, recipe=recipe).exists():
        Cart.objects.create(user=request.user, recipe=recipe)
    return JsonResponse({'success': True})


@login_required
def remove_from_list(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    cart = Cart.objects.filter(user=request.user, recipe=recipe)
    cart.delete()
    return JsonResponse({'success': False})


@login_required
def remove_from_cart(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    cart = Cart.objects.filter(user=request.user, recipe=recipe)
    cart.delete()
    return redirect(reverse('shoplist'))


def download_pdf_ingredients(request):
    all_ingredients = union_ingredients(request)
    buffer = make_pdf(all_ingredients)

    return FileResponse(buffer, as_attachment=True, filename='to_buy.pdf')
