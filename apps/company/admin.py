from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Sector, ActivityArea, Company, Facilities


@admin.register(Sector)
class SectorAdmin(TranslatableAdmin):
    list_display = ('name', 'description')


@admin.register(ActivityArea)
class ActivityAreaAdmin(TranslatableAdmin):
    list_display = ('sector', 'name', 'description')


@admin.register(Company)
class CompanyAdmin(TranslatableAdmin):
    list_display = ('name', 'description', 'address')


@admin.register(Facilities)
class CompanyAdmin(TranslatableAdmin):
    list_display = ('company', 'name', 'description', 'address')