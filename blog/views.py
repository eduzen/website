import datetime as dt
from typing import Any

import logfire
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django_filters.views import FilterView

from .filters import PostFilter
from .forms import AdvanceSearchForm, ContactForm
from .models import Post
from .services.parsers import apply_styles
from .services.telegram import send_contact_message

MIN = 60
HOUR = 60 * MIN
DAY = 24 * HOUR
MONTH = 30 * DAY
HALF_YEAR = 6 * MONTH


@login_required
def post_update_styles(request: HttpRequest, post_id: int) -> HttpResponse:
    """Apply styles to a post using BeautifulSoup."""
    post = get_object_or_404(Post, pk=post_id)
    post.text = apply_styles(post.text)
    post.save()
    return redirect("admin:blog_post_change", post_id)


class HtmxGetMixin:
    partial_template_name: str

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.htmx and self.partial_template_name:  # type: ignore
            self.template_name = self.partial_template_name
        return super().get(request, *args, **kwargs)  # type: ignore

    def get_template_names(self):
        """Return the correct template based on the request type (HTMX or regular)."""
        if self.request.htmx:
            return [self.partial_template_name]
        return [self.template_name]


@method_decorator(cache_page(MONTH), name="dispatch")
class AboutView(HtmxGetMixin, TemplateView):
    template_name = "blog/about.html"
    partial_template_name = "blog/partials/about.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        start_year = 2014
        current_year = dt.datetime.now().year
        context["years_of_experience"] = current_year - start_year
        return context


class SuccessView(TemplateView):
    template_name = "blog/success.html"


class ErrorView(TemplateView):
    template_name = "blog/error.html"


class AdvanceSearch(FormView):
    template_name = "blog/search.html"
    form_class = AdvanceSearchForm
    success_url = "/sucess/"


@method_decorator(cache_page(MONTH), name="dispatch")
class HomeView(HtmxGetMixin, TemplateView):
    template_name = "blog/home.html"
    partial_template_name = "blog/partials/home.html"


@method_decorator(cache_page(MONTH), name="dispatch")
class ConsultancyView(HtmxGetMixin, TemplateView):
    template_name = "blog/consultancy.html"
    partial_template_name = "blog/partials/consultancy.html"


@method_decorator(cache_page(MONTH), name="dispatch")
class ClassesView(HtmxGetMixin, TemplateView):
    template_name = "blog/classes.html"
    partial_template_name = "blog/partials/classes.html"


@method_decorator(cache_page(MONTH), name="dispatch")
class PostListView(HtmxGetMixin, FilterView):
    queryset = Post.objects.published().prefetch_related("tags")
    context_object_name = "posts"
    template_name = "blog/posts/list.html"
    partial_template_name = "blog/partials/posts/list.html"
    ordering = ["-published_date"]
    filterset_class = PostFilter
    paginate_by = 12


@method_decorator(cache_page(MONTH), name="dispatch")
class PostTagsListView(HtmxGetMixin, FilterView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/posts/list.html"
    partial_template_name = "blog/partials/posts/list.html"
    ordering = ["-published_date"]
    filterset_class = PostFilter
    paginate_by = 12

    def get_context_data(self, object_list=None, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["tag"] = self.kwargs.get("tag", "-").title()
        return context

    def get_queryset(self) -> QuerySet[Post]:
        return self.queryset.filter(tags__slug=self.kwargs.get("tag"))


@method_decorator(cache_page(MONTH), name="dispatch")
class PostDetailView(HtmxGetMixin, DetailView):
    queryset = Post.objects.prefetch_related("tags").published()
    context_object_name = "post"
    template_name = "blog/posts/detail.html"
    partial_template_name = "blog/partials/posts/detail.html"


@method_decorator(cache_page(MONTH), name="dispatch")
class RelatedPostsView(HtmxGetMixin, ListView):
    template_name = "blog/partials/posts/related_posts.html"
    partial_template_name = "blog/partials/posts/related_posts.html"
    context_object_name = "related_posts"
    paginate_by = 4

    def get_queryset(self) -> QuerySet[Post]:
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)

        tag_ids = post.tags.values_list("id", flat=True)
        related_posts = (
            Post.objects.published()
            .filter(tags__id__in=tag_ids)
            .order_by("-published_date")
            .distinct()
            .exclude(pk=post.pk)
        )

        return related_posts

    def get_context_data(self, object_list=None, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["post_id"] = self.kwargs.get("post_id")
        return context


class ContactView(HtmxGetMixin, FormView):
    template_name = "blog/contact.html"
    partial_template_name = "blog/partials/contact.html"
    form_class = ContactForm
    error_url = reverse_lazy("error")

    def form_valid(self, form):
        context = {
            "name": form.cleaned_data["name"],
            "email": form.cleaned_data["email"],
            "message": form.cleaned_data["message"],
        }

        try:
            response = send_contact_message(**context)
            logfire.info(response)
        except Exception:
            logfire.exception("Contact problems")
            return redirect(self.error_url)

        return render(self.request, "blog/success.html", context)

    def form_invalid(self, form: ContactForm):
        context_data = self.get_context_data(form=form)
        return render(self.request, self.partial_template_name, context_data)
