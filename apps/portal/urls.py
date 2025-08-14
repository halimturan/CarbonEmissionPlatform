from django.urls import path, include
from apps.portal.views import *
from django.utils.translation import gettext_lazy as _

app_name = 'portal'

urlpatterns = [
    path('', index, name='index'),
    path(_('uye_ol'), sign_up, name='sign_up'),
    path('sirket/', include('apps.company.urls')),
]
