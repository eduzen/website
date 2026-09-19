from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import TemplateResponseMixin

from .htmx import is_htmx_fragment_request


class MissingTemplateNameError(ImproperlyConfigured):
    def __init__(self, view_name: str) -> None:
        super().__init__(f"{view_name} requires `template_name`.")


class HtmxGetMixin(TemplateResponseMixin):
    """
    Handle HTMX requests by swapping to partial templates.
    Follows django-htmx recommended pattern for base template swapping.
    """

    template_name: str | None = None
    partial_template_name: str | None = None

    def get_template_names(self) -> list[str]:
        if is_htmx_fragment_request(self.request) and self.partial_template_name:
            return [self.partial_template_name]

        if self.template_name:
            return [self.template_name]

        raise MissingTemplateNameError(self.__class__.__name__)
