from types import SimpleNamespace

import pytest
from django.core.exceptions import ImproperlyConfigured

from core.mixins import HtmxGetMixin


class _DummyHtmxView(HtmxGetMixin):
    template_name = "core/full.html"
    partial_template_name = "core/partial.html"


class _DummyNoPartialView(HtmxGetMixin):
    template_name = "core/full.html"
    partial_template_name = None


class _DummyNoTemplateView(HtmxGetMixin):
    template_name = None
    partial_template_name = None


class _DummyHtmxDetails:
    history_restore_request: bool

    def __init__(self, *, history_restore_request: bool = False) -> None:
        self.history_restore_request = history_restore_request

    def __bool__(self) -> bool:
        return True


def test_get_template_names_uses_partial_for_htmx_request():
    view = _DummyHtmxView()
    view.request = SimpleNamespace(htmx=True)

    assert view.get_template_names() == ["core/partial.html"]


def test_get_template_names_uses_full_template_for_htmx_history_restore_request():
    view = _DummyHtmxView()
    view.request = SimpleNamespace(htmx=_DummyHtmxDetails(history_restore_request=True))

    assert view.get_template_names() == ["core/full.html"]


def test_get_template_names_uses_full_template_for_normal_request():
    view = _DummyHtmxView()
    view.request = SimpleNamespace(htmx=False)

    assert view.get_template_names() == ["core/full.html"]


def test_get_template_names_falls_back_when_partial_missing():
    view = _DummyNoPartialView()
    view.request = SimpleNamespace(htmx=True)

    assert view.get_template_names() == ["core/full.html"]


def test_get_template_names_raises_without_template_name():
    view = _DummyNoTemplateView()
    view.request = SimpleNamespace(htmx=False)

    with pytest.raises(ImproperlyConfigured):
        view.get_template_names()
