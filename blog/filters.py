import django_filters
from django.contrib.postgres.search import SearchVector
from django.db.models import QuerySet

from blog.models import Post


class PostFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search", label="Search")

    class Meta:
        model = Post

    def filter_search(self, queryset: QuerySet[Post], name: str, value: str) -> QuerySet[Post]:
        search_vector = SearchVector("text", "title", "summary")
        return queryset.annotate(search=search_vector).filter(search=value)
