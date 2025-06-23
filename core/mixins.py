from typing import cast

from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import TemplateResponseMixin

from .types import HtmxHttpRequest


class HtmxGetMixin(TemplateResponseMixin):
    """
    Handle HTMX requests by swapping to partial templates.
    Follows django-htmx recommended pattern for base template swapping.
    """

    template_name: str | None = None
    partial_template_name: str | None = None

    def get_template_names(self) -> list[str]:
        request = cast(HtmxHttpRequest, self.request)

        # For HTMX requests, render just the partial template
        if request.htmx and self.partial_template_name:
            return [self.partial_template_name]

        if self.template_name:
            return [self.template_name]

        raise ImproperlyConfigured(f"{self.__class__.__name__} requires `template_name`.")
