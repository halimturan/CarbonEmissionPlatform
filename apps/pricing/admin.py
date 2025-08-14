from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Plan, Features, PlanFeature, Organization


@admin.register(Plan)
class PlanAdmin(TranslatableAdmin):
    list_display = ('name', 'price', 'is_active', 'alignment')
    list_editable = ['price', 'is_active', 'alignment']


@admin.register(Features)
class FeaturesAdmin(TranslatableAdmin):
    list_display = ('name', 'description', 'is_active', 'alignment')
    list_editable = ['is_active', 'alignment']


@admin.register(PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = ('plan', 'feature', 'limit')
    list_editable = ['limit',]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
