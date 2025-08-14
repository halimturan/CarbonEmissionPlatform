from django.urls import path
from apps.company.views.check_company_of_user import check_company_of_user
from apps.company.views.overview import overview
from django.utils.translation import gettext_lazy as _

app_name = 'company'

urlpatterns = [
    path(_('genel_bakis/'), overview, name='overview'),
    path('check_user_of_company', check_company_of_user, name='check_company_of_user'),
]
