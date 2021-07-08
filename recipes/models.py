from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=256, verbose_name='ingredient name')
    units = models.CharField(max_length=64, verbose_name='uits')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'name',
                    'units'],
                name='unique ingredient'),
        ]
        verbose_name_plural = 'Ингредиент'

    def __str__(self):
        return f'{self.name}({self.units})'


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='tagname')
    color = models.CharField(max_length=100, blank=True,
                             verbose_name='tagcolor', default='')

    class Meta:
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):

    def validate_zero(value):
        if value == 0:
            raise ValidationError(
                _('Время пиготовления должно быть больше нуля'),
            )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='author')
    title = models.CharField(max_length=256, verbose_name='recipe name')
    image = models.ImageField(verbose_name='recipe picture', blank=True, null=False)
    description = models.TextField(verbose_name='recipe description')
    cooking_time = models.PositiveIntegerField(
        validators=[validate_zero],
        help_text='min',
        verbose_name='cooking time')
    ingredients = models.ManyToManyField(Ingredient, through='IngredientRecipe', verbose_name='ingredients')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='tags')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='pub date'
    )

    class Meta:
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return 'Рецепт: {}'.format(self.title)


class IngredientRecipe(models.Model):

    def validate_zero(value):
        if value <= 0:
            raise ValidationError(
                _('Значение должно быть больше нуля'),
            )

    ingredient = models.ForeignKey(Ingredient, on_delete=CASCADE, verbose_name='ingredient')
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE, related_name='ingredient_recipe', verbose_name='recipe')
    value = models.FloatField(validators=[validate_zero], help_text='вставить ед.изм', verbose_name='value')

    class Meta:
        verbose_name_plural = 'Ингредиенты в рецептах'

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
        verbose_name_plural = 'Подписки'


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
        verbose_name_plural = 'Избранное'


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
        verbose_name_plural = 'Корзина'
