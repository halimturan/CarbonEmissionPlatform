from django.urls import path
from apps.pricing.views import *
from django.utils.translation import gettext_lazy as _

app_name = 'pricing'

urlpatterns = [
    path(_('odeme/<str:slug>'), payment, name='payment'),
    path(_('planlar'), plans, name='plans'),
]
