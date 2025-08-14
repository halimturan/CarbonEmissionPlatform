import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarbonEmissionPlatform.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "CarbonEmissionPlatform.settings"
django.setup()
from apps.web.models import Country

with (open('countries.csv', mode='r', newline='', encoding='utf-8') as csvfile):
    data = list(csv.DictReader(csvfile))
    for i in data:
        country_id = i.get('id')
        country_name = i.get('name')
        iso2 = i.get('iso2')
        emoji = i.get('emoji')
        print(country_id, country_name, iso2, emoji)
        Country.objects.get_or_create(country_id=country_id, name=country_name, iso2=iso2, emoji=emoji)