# Generated by Django 3.2.3 on 2021-05-17 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20210517_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='recipes/images/', verbose_name='Фото рецепта'),
        ),
    ]