import logging
from typing import Any

from constance import config
from django import http
from django.contrib.postgres.search import SearchVector
from django.db.models import QuerySet
from django.forms import ModelForm
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, FormView, ListView, TemplateView

from .forms import AdvanceSearchForm, EmailForm, SearchForm
from .models import Post

logger = logging.getLogger(__name__)

MIN = 60
HOUR = 60 * MIN
DAY = 24 * HOUR


class ConfigMixin:
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)  # type: ignore
        context["config"] = config
        return context


@method_decorator(cache_page(DAY), name="dispatch")
class AboutView(ConfigMixin, TemplateView):
    template_name = "blog/about.html"


@method_decorator(cache_page(DAY), name="dispatch")
class SucessView(TemplateView):
    template_name = "blog/success.html"


@method_decorator(cache_page(DAY), name="dispatch")
class ErrorView(TemplateView):
    template_name = "blog/error.html"


class AdvanceSearch(FormView):
    template_name = "blog/advance_search.html"
    form_class = AdvanceSearchForm
    success_url = "/sucess/"


@method_decorator(cache_page(HOUR), name="dispatch")
class HomeListView(ListView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/home.html"
    ordering = ["-published_date"]
    paginate_by = 12

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tags"] = Post.objects.count_tags()
        context["search_form"] = SearchForm()
        return context


@method_decorator(cache_page(HOUR), name="dispatch")
class PostListView(ListView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/home.html"
    ordering = ["-published_date"]
    paginate_by = 12

    def get_queryset(self) -> QuerySet[Post]:
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if not query:
            return queryset

        return queryset.annotate(search=SearchVector("text", "title", "pompadour")).filter(search=query)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm()
        context["tags"] = Post.objects.count_tags()
        context["tag"] = self.request.GET.get("q", "")
        return context

    def render_to_response(self, context: dict[str, Any]) -> http.HttpResponse:
        posts = context.get("posts")
        if not posts:
            return redirect("search")

        return super().render_to_response(context)


@method_decorator(cache_page(HOUR), name="dispatch")
class PostTagsList(ListView):
    model = Post
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/home.html"
    ordering = ["-published_date"]
    paginate_by = 10

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tags"] = Post.objects.count_tags()
        context["search_form"] = SearchForm()
        context["tag"] = self.kwargs.get("tag").title()
        return context

    def get_queryset(self) -> QuerySet[Post]:
        return self.queryset.filter(tags__slug=self.kwargs.get("tag"))


@method_decorator(cache_page(DAY), name="dispatch")
class PostDetail(DetailView):
    queryset = Post.objects.prefetch_related("tags").published()
    context_object_name = "post"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        context["related_posts"] = (
            Post.objects.published()
            .filter(tags__in=self.object.tags.all())
            .order_by("-published_date")
            .distinct()
            .exclude(pk=self.object.pk)[:15]
        )
        return context


@method_decorator(cache_page(DAY), name="get")
class ContactView(ConfigMixin, FormView):
    template_name = "blog/contact.html"
    form_class = EmailForm
    success_url = "/sucess/"

    def form_valid(self, form: ModelForm):
        try:
            form.send_email()
            return super().form_valid(form)
        except Exception:
            logger.exception("Email problems")

        return redirect("/error/")


class Google(TemplateView):
    template_name = "blog/google.html"
