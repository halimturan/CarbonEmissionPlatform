from django.contrib.sitemaps import Sitemap
from apps.api.models import Category


class ProductsSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Category.objects.all()

    def location(self, obj: Category) -> str:
        return obj.get_absolute_url()
