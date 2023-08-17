from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.urls import reverse

from blog.models import Post


class StaticViewSitemap(Sitemap):
    """Sitemap for improving google indexing"""

    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["home", "blog", "about", "contact"]

    def location(self, obj):
        return reverse(obj)


INFO_DICT = {"queryset": Post.objects.filter(published_date__isnull=False), "date_field": "published_date"}


sitemaps = {"static": StaticViewSitemap, "blog": GenericSitemap(INFO_DICT, priority=0.6)}  # type: ignore
