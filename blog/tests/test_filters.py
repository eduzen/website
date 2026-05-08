from unittest.mock import Mock, patch

from blog.filters import PostFilter


def test_filter_search_returns_original_queryset_for_blank_value() -> None:
    filterset = PostFilter()
    queryset = Mock()

    assert filterset.filter_search(queryset, "q", "") is queryset
    assert filterset.filter_search(queryset, "q", "   ") is queryset

    queryset.filter.assert_not_called()


def test_filter_search_applies_ranked_search_for_value() -> None:
    filterset = PostFilter()
    queryset = Mock(name="queryset")
    filtered_queryset = Mock(name="filtered_queryset")
    annotated_queryset = Mock(name="annotated_queryset")

    queryset.filter.return_value = filtered_queryset
    filtered_queryset.annotate.return_value = annotated_queryset
    annotated_queryset.order_by.return_value = "ordered"

    with patch("blog.filters.SearchQuery", return_value="search-query") as mock_search_query:
        with patch("blog.filters.SearchRank", return_value="search-rank") as mock_search_rank:
            result = filterset.filter_search(queryset, "q", "django")

    assert result == "ordered"
    mock_search_query.assert_called_once_with("django")
    queryset.filter.assert_called_once_with(search_vector="search-query")
    mock_search_rank.assert_called_once_with("search_vector", "search-query")
    filtered_queryset.annotate.assert_called_once_with(rank="search-rank")
    annotated_queryset.order_by.assert_called_once_with("-rank")
