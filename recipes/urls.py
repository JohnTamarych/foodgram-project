from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe', views.recipe, name='recipe'),
    path('recipe/<int:recipe_id>/', views.single_recipe, name='single'),
]