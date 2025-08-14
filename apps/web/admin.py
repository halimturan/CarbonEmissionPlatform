from django.contrib import admin
from parler.admin import TranslatableAdmin
from apps.web.models import (Sliders, MenuItem, SubMenu, FAQ, WhyUse, Features, ContentBlock)


@admin.register(MenuItem)
class MenuItemAdmin(TranslatableAdmin):
    list_display = ('title', 'alignment', 'link')
    list_editable = ['alignment',]


@admin.register(SubMenu)
class SubMenuAdmin(TranslatableAdmin):
    list_display = ('title', 'alignment', 'link')
    list_editable = ['alignment', 'link']


@admin.register(Sliders)
class SlidersAdmin(TranslatableAdmin):
    list_display = ('text', 'alignment', 'is_publish')
    list_editable = ['alignment', 'is_publish']


@admin.register(FAQ)
class FAQAdmin(TranslatableAdmin):
    list_display = ('question', 'answer', 'alignment')
    list_editable = ['alignment',]


@admin.register(WhyUse)
class WhyUseAdmin(TranslatableAdmin):
    list_display = ('title', 'description', 'alignment')
    list_editable = ['alignment',]


@admin.register(Features)
class FeaturesAdmin(TranslatableAdmin):
    list_display = ('title', 'alignment')
    list_editable = ['alignment', ]


@admin.register(ContentBlock)
class ContentBlockAdmin(TranslatableAdmin):
    list_display = ('text',)