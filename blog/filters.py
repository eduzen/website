import django_filters
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import QuerySet

from blog.models import Post


class PostFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search", label="Search")

    class Meta:
        model = Post
        fields = ["q"]

    def filter_search(self, queryset: QuerySet[Post], name: str, value: str) -> QuerySet[Post]:
        if not value or not value.strip():
            return queryset

        search_query = SearchQuery(value)
        return (
            queryset.filter(search_vector=search_query)
            .annotate(rank=SearchRank("search_vector", search_query))
            .order_by("-rank")
        )
