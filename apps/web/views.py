from django.http import JsonResponse
from django.shortcuts import render
from apps.web.models import Sliders, MenuItem, FAQ, WhyUse, Features, ContentBlock, Country, City
from apps.pricing.models import Plan
import json
from django.core.serializers import serialize

def index(request):
    sliders = Sliders.objects.all()
    faq = FAQ.objects.all()
    why_use = WhyUse.objects.all()
    features = Features.objects.all()
    content_block = ContentBlock.objects.last()
    pricing = Plan.objects.all()
    context = {
        'sliders': sliders,
        'menu_items': MenuItem.objects.all(),
        'faq': faq,
        'why_use': why_use,
        'features': features,
        'content_block': content_block,
        'pricing': pricing,
    }
    return render(request, 'web/index.html', context)


def get_countries(request):
    countries = json.loads(serialize('json', Country.objects.all()))
    return JsonResponse(countries, safe=False)


def get_cities(request, country_id):
    cities = json.loads(serialize('json', City.objects.filter(country_id=country_id)))
    return JsonResponse(cities, safe=False)


def contact(request):
    return render(request, 'web/contact.html')
