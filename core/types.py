from typing import TYPE_CHECKING

from django.http import HttpRequest as HttpRequestBase

if TYPE_CHECKING:
    from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequestBase):
    htmx: "HtmxDetails"
