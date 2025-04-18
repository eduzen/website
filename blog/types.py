# blog/types.py
from django.http import HttpRequest as HttpRequestBase
from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequestBase):
    """
    Extend Django’s HttpRequest so that mypy/pyright know
    there’s an `.htmx: HtmxDetails` attribute on it.
    """

    htmx: HtmxDetails
