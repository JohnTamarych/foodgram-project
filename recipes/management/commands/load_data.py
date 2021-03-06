import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        with open('recipes/data/ingredients.csv') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                row = row[0].split(';')
                name = row[0]
                unit = row[-1]
                Ingredient.objects.get_or_create(name=name, units=unit)
