from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from django.db.models.fields.files import ImageField

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название ингредиента')
    unit = models.CharField(max_length=64, verbose_name='Единицы измерения')

    def __str__(self):
        return '{}({})'.format(self.name, self.unit)


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='tagname')
    color = models.CharField(max_length=100, blank=True,
                             verbose_name='tagcolor', default='')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=CASCADE, verbose_name='Автор рецепта')
    title = models.CharField(max_length=256, verbose_name='Название рецепта')
    image = models.ImageField(upload_to='recipes/images/', verbose_name='Фото рецепта', blank=True, null=True)
    description = models.TextField(verbose_name='Описание рецепта')
    cooking_time = models.PositiveIntegerField(help_text='min', verbose_name='Время приготовления')
    ingredients = models.ManyToManyField(Ingredient, through='IngredientRecipe', verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='tags')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    def __str__(self):
        return 'Рецепт: {}'.format(self.title)


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE, verbose_name='Рецепт')
    value = models.FloatField(help_text='вставить ед.изм', verbose_name='Количество')

    def __str__(self):
        return 'Ингредиент {}'.format(self.recipe)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'author'],
                name='unique follow'),
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_user',
        verbose_name='user')
    recipe = models.ForeignKey(
        Recipe, 
        blank=True,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        default='',
        verbose_name='favorites')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe'],
                name='unique favorite'),
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_purchases',
        verbose_name='user')
    recipe = models.ForeignKey(
        Recipe, blank=True,
        on_delete=models.CASCADE,
        related_name='listed_recipes',
        default='',
        verbose_name='listed_recipes')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe'],
                name='unique cart'),
        ]