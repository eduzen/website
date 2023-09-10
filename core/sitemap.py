from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.urls import reverse
from django.db.models import QuerySet

from blog.models import Post


class StaticViewSitemap(Sitemap):
    """Sitemap for improving google indexing"""

    priority: float = 0.5
    changefreq: str = "daily"

    def items(self) -> list[str]:
        return ["home", "blog", "about", "contact", "consultancy", "classes", "search"]

    def location(self, obj: str) -> str | None:  # type: ignore
        return reverse(obj)


INFO_DICT: dict[str, type[Post] | str | QuerySet[Post]] = {
    "queryset": Post.objects.filter(published_date__isnull=False),
    "date_field": "published_date",
}

sitemaps: dict[str, type[StaticViewSitemap] | GenericSitemap] = {
    "static": StaticViewSitemap,
    "blog": GenericSitemap(INFO_DICT, priority=0.6),  # type: ignore
}
