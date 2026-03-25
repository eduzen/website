from collections.abc import Mapping

from django import template

register = template.Library()


@register.filter
def dict_get(dictionary: Mapping[object, object], key: object) -> object | None:
    return dictionary.get(key, None)
