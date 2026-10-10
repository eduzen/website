from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag
def windowed_page_range(paginator: Paginator, current_page: int, window: int = 2) -> list[int | None]:
    """
    Return an ordered list of page numbers with ``None`` as a sentinel for
    ellipsis gaps.  Always includes the first and last page, plus ``window``
    pages on each side of ``current_page``.

    Example (current=6, window=2, total=20):
        [1, None, 4, 5, 6, 7, 8, None, 20]
    """
    num_pages = paginator.num_pages
    if num_pages <= 1:
        return [1]

    visible = {1, num_pages}
    visible.update(range(max(1, current_page - window), min(num_pages, current_page + window) + 1))

    result: list[int | None] = []
    prev: int | None = None
    for p in sorted(visible):
        if prev is not None and p - prev > 1:
            result.append(None)  # ellipsis placeholder
        result.append(p)
        prev = p

    return result
