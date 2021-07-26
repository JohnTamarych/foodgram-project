from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название ингредиента')
    units = models.CharField(max_length=64, verbose_name='Единицы измерения')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'name',
                    'units'],
                name='unique ingredient'),
        ]
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиент'

    def __str__(self):
        return f'{self.name}({self.units})'


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя тега')
    color = models.CharField(max_length=100, blank=True,
                             verbose_name='Цвет тега', default='')

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор')
    title = models.CharField(max_length=256, verbose_name='Название рецепта')
    image = models.ImageField(verbose_name='Фото рецепта', blank=True, null=False)
    description = models.TextField(verbose_name='Описание рецепта')
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1, 'Время приготовления должно быть больше нуля')],
        help_text='min',
        verbose_name='Время приготовления')
    ingredients = models.ManyToManyField(Ingredient, through='IngredientRecipe', verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return 'Рецепт: {}'.format(self.title)


class IngredientRecipe(models.Model):

    ingredient = models.ForeignKey(Ingredient, on_delete=CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE, related_name='ingredient_recipe', verbose_name='Рецепт')
    value = models.FloatField(
        validators=[MinValueValidator(0.001, 'Добавьте побольше ингредиентов')],
        help_text='Количество ингредиента',
        verbose_name='Количество'
        )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return 'Ингредиент {}'.format(self.recipe)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Предмет подписки')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'author'],
                name='unique follow'),
        ]
        verbose_name = 'подписку'
        verbose_name_plural = 'Подписки'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_user',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        blank=True,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        default='',
        verbose_name='Избранное')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe'],
                name='unique favorite'),
        ]
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'Избранное'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_purchases',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe, blank=True,
        on_delete=models.CASCADE,
        related_name='listed_recipes',
        default='',
        verbose_name='Список рецептов')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe'],
                name='unique cart'),
        ]
        verbose_name_plural = 'Корзина'
