from django import template

register = template.Library()


@register.inclusion_tag("blog/extras/paginator.html")
def show_paginator(page_obj):
    pages = range(1, page_obj.paginator.num_pages + 1)
    return {"pages": pages, "page_obj": page_obj}
