# Generated by Django 3.2.3 on 2021-06-07 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipe_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='tagname')),
                ('color', models.CharField(blank=True, default='', max_length=100, verbose_name='tagcolor')),
            ],
        ),
    ]
