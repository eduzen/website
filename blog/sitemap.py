from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import GenericSitemap
from django.urls import reverse

from .models import Post


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["home", "blog", "about", "clases", "contact"]

    def location(self, item):
        return reverse(item)


info_dict = {
    "queryset": Post.objects.filter(published_date__isnull=False),
    "date_field": "published_date",
}


sitemaps = {"static": StaticViewSitemap, "blog": GenericSitemap(info_dict, priority=0.6)}
