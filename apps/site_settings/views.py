from apps.site_settings.models import (SiteSettings)
from apps.web.models import MenuItem


def context(request):
    if 'super/user' in request.path:
        return {}
    site_settings = SiteSettings.objects.last()
    return {
        "site_settings": site_settings,
        'menu_items': MenuItem.objects.all(),
    }
