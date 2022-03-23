import csv

from django.core.management.base import BaseCommand

from main.models import City
from main.serializers import CitySerializer


class Command(BaseCommand):
    help = "Парсинг csv и сохранение в БД"

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        City.objects.all().delete()

        for i, row in enumerate(csv.DictReader(open(options["file"][0], encoding='utf-8'))):
            serializer = CitySerializer(data=row)
            if serializer.is_valid():
                serializer.save()
            print(f"{i} {'SUCCESS' if serializer.is_valid() else f'ERROR {serializer.errors}'}")

