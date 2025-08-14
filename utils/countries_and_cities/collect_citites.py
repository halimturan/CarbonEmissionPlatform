import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarbonEmissionPlatform.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "CarbonEmissionPlatform.settings"
django.setup()
from apps.web.models import City

with (open('cities.csv', mode='r', newline='', encoding='utf-8') as csvfile):
    data = list(csv.DictReader(csvfile))
    for i in data:
        name = i.get('name')
        country_id = i.get('country_id')
        City.objects.get_or_create(country_id=country_id, name=name)
