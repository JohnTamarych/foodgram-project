# Generated by Django 3.2.3 on 2021-06-11 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Фото рецепта'),
        ),
    ]