from typing import Any, cast

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Page, Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.base import View
from django.views.generic.list import MultipleObjectMixin
from django_filters.views import FilterView

from core.htmx import is_htmx_fragment_request

from .filters import PostFilter
from .forms import AdvanceSearchForm
from .models import Post
from .services.parsers import apply_styles


class HtmxPartialTemplateMixin:
    htmx_template_name: str | None = None
    request: HttpRequest
    template_name: str

    def get_template_names(self) -> list[str]:
        if is_htmx_fragment_request(self.request) and self.htmx_template_name:
            return [self.htmx_template_name]
        return [self.template_name]


class SafePaginationMixin(MultipleObjectMixin, View):
    """Redirect invalid page numbers to page 1 and out-of-range pages to the last page."""

    _redirect_url: str | None = None

    def _page_url(self, page_number: int) -> str:
        query_params = self.request.GET.copy()
        query_params[self.page_kwarg] = str(page_number)
        return f"{self.request.path}?{query_params.urlencode()}"

    def paginate_queryset(self, queryset: object, page_size: int) -> tuple[Paginator, Page[Post], QuerySet[Post], bool]:
        paginator = self.get_paginator(
            cast(QuerySet[Post], queryset),
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        page = self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or 1

        try:
            page_number = int(page)
        except ValueError, TypeError:
            page_number = 1
            self._redirect_url = self._page_url(page_number)

        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            page_number = max(paginator.num_pages, 1)
            self._redirect_url = self._page_url(page_number)
            page_obj = paginator.page(page_number)

        object_list = cast(QuerySet[Post], page_obj.object_list)
        return (paginator, page_obj, object_list, page_obj.has_other_pages())

    def get(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
        response = super().get(request, *args, **kwargs)  # type: ignore[misc]
        if self._redirect_url:
            return redirect(self._redirect_url)
        return response


@login_required
def post_update_styles(request: HttpRequest, post_id: int) -> HttpResponse:
    """Apply styles to a post using BeautifulSoup."""
    post = get_object_or_404(Post, pk=post_id)
    post.text = apply_styles(post.text)
    post.save()
    return redirect("admin:blog_post_change", post_id)


class AboutView(HtmxPartialTemplateMixin, TemplateView):
    """About page. Dynamic values (years_in_python, years_of_experience)
    come from the global_data context processor — no need to duplicate here."""

    template_name = "blog/about.html"
    htmx_template_name = "blog/about.html#about-content"


class SuccessView(HtmxPartialTemplateMixin, TemplateView):
    template_name = "blog/success.html"
    htmx_template_name = "blog/success.html#success-content"


class ErrorView(HtmxPartialTemplateMixin, TemplateView):
    template_name = "blog/error.html"
    htmx_template_name = "blog/error.html#error-content"


class AdvanceSearch(HtmxPartialTemplateMixin, FormView):
    template_name = "blog/search.html"
    htmx_template_name = "blog/search.html#search-content"
    form_class = AdvanceSearchForm
    success_url = "/success/"


class HomeView(HtmxPartialTemplateMixin, TemplateView):
    template_name = "blog/home.html"
    htmx_template_name = "blog/home.html#home-content"


class WorkView(HtmxPartialTemplateMixin, TemplateView):
    template_name = "blog/work.html"
    htmx_template_name = "blog/work.html#work-content"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        context = super().get_context_data(**kwargs)
        context["projects"] = [
            {
                "name": "Maiteblog",
                "url": "https://maiteblog.com",
                "description": (
                    "A personal baby tracker for the moments that matter. "
                    "Log feeds, diapers, sleep, and more in one tap-friendly view."
                ),
                "tags": ["Django", "React", "Python"],
                "image": "core/img/work/maiteblog.jpg",
            },
            {
                "name": "GroomIt",
                "url": "https://groomit.io",
                "description": (
                    "Turn sprint retrospectives into engaging sessions "
                    "where agile teams reflect, learn, and grow together."
                ),
                "tags": ["FastAPI", "React", "Python"],
                "image": "core/img/work/groomit.jpg",
            },
            {
                "name": "Champi",
                "url": "https://champi.dev",
                "description": (
                    "Restaurant management platform — access, teams, and operations organized by role and context."
                ),
                "tags": ["Django", "React", "Python"],
                "image": "core/img/work/champi.jpg",
            },
            {
                "name": "Althaia",
                "url": "https://althaia.nl",
                "description": "Website for a Dutch wellness brand. Currently under construction.",
                "tags": ["Django", "HTMX", "Python"],
                "image": "core/img/work/althaia.jpg",
            },
        ]
        return context


class ConsultancyView(HtmxPartialTemplateMixin, TemplateView):
    template_name = "blog/consultancy.html"
    htmx_template_name = "blog/consultancy.html#consultancy-content"


class ClassesView(HtmxPartialTemplateMixin, TemplateView):
    template_name = "blog/classes.html"
    htmx_template_name = "blog/classes.html#classes-content"


class MentoringView(HtmxPartialTemplateMixin, TemplateView):
    template_name = "blog/mentoring.html"
    htmx_template_name = "blog/mentoring.html#mentoring-content"


class PostListView(HtmxPartialTemplateMixin, SafePaginationMixin, FilterView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/posts/list.html"
    htmx_template_name = "blog/posts/list.html#posts-list-content"
    ordering = ["-published_date"]
    filterset_class = PostFilter
    paginate_by = 12


class PostTagsListView(PostListView):
    def get_context_data(self, *, object_list: object | None = None, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        context = super().get_context_data(object_list=cast(Any, object_list), **kwargs)
        context["tag"] = self.kwargs.get("tag", "-").title()
        return context

    def get_queryset(self) -> QuerySet[Post]:
        return self.queryset.filter(tags__slug__iexact=self.kwargs.get("tag"))


class PostDetailView(HtmxPartialTemplateMixin, DetailView):
    queryset = Post.objects.select_related("author").prefetch_related("tags").published()
    context_object_name = "post"
    template_name = "blog/posts/detail.html"
    htmx_template_name = "blog/posts/detail.html#post-detail-content"


class RelatedPostsView(HtmxPartialTemplateMixin, ListView):
    template_name = "blog/posts/related_posts.html"
    htmx_template_name = "blog/posts/related_posts.html#related-posts-content"
    context_object_name = "related_posts"
    paginate_by = 4

    def get_queryset(self) -> QuerySet[Post]:
        post_id = self.kwargs.get("post_id")
        tag_ids = Post.objects.filter(pk=post_id).values("tags__id")
        return (
            Post.objects.filter(published_date__isnull=False)
            .filter(tags__id__in=tag_ids)
            .exclude(pk=post_id)
            .distinct()
            .order_by("-published_date")
        )

    def get_context_data(self, *, object_list: object | None = None, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        context = super().get_context_data(object_list=cast(Any, object_list), **kwargs)
        context["post_id"] = self.kwargs.get("post_id")
        return context


class ContactView(HtmxPartialTemplateMixin, TemplateView):
    template_name = "blog/contact.html"
    htmx_template_name = "blog/contact.html#contact-content"
