from django.urls import path
from apps.web.views import *
from django.utils.translation import gettext_lazy as _

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path(_('iletisim'), contact, name='contact'),
    path('get_countries/', get_countries, name='get_countries'),
    path('get_cities/<int:country_id>/', get_cities, name='get_cities'),
]
