import datetime as dt
import logging
from typing import Any

from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django_filters.views import FilterView

from .filters import PostFilter
from .forms import AdvanceSearchForm, ContactForm
from .models import Post
from .services.parsers import apply_styles
from .services.telegram import send_contact_message

logger = logging.getLogger(__name__)


@login_required
def post_update_styles(request: HttpRequest, post_id: int) -> HttpResponse:
    """Apply styles to a post using BeautifulSoup."""
    post = get_object_or_404(Post, pk=post_id)
    post.text = apply_styles(post.text)
    post.save()
    return redirect("admin:blog_post_change", post_id)


class AboutView(TemplateView):
    template_name = "blog/about.html"

    def get_template_names(self):
        if self.request.htmx:
            return ["blog/about.html#about-content"]
        return [self.template_name]

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
    success_url = "/success/"


class HomeView(TemplateView):
    template_name = "blog/home.html"

    def get_template_names(self):
        if self.request.htmx:
            return ["blog/home.html#home-content"]
        return [self.template_name]


class ConsultancyView(TemplateView):
    template_name = "blog/consultancy.html"

    def get_template_names(self):
        if self.request.htmx:
            return ["blog/consultancy.html#consultancy-content"]
        return [self.template_name]


class ClassesView(TemplateView):
    template_name = "blog/classes.html"

    def get_template_names(self):
        if self.request.htmx:
            return ["blog/classes.html#classes-content"]
        return [self.template_name]


class PostListView(FilterView):
    queryset = Post.objects.published().prefetch_related("tags")
    context_object_name = "posts"
    template_name = "blog/posts/list.html"
    ordering = ["-published_date"]
    filterset_class = PostFilter
    paginate_by = 12

    def get_template_names(self):
        if self.request.htmx:
            return ["blog/posts/list.html#posts-list-content"]
        return [self.template_name]


class PostTagsListView(FilterView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/posts/list.html"
    ordering = ["-published_date"]
    filterset_class = PostFilter
    paginate_by = 12

    def get_template_names(self):
        if self.request.htmx:
            return ["blog/posts/list.html#posts-list-content"]
        return [self.template_name]

    def get_context_data(self, object_list=None, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["tag"] = self.kwargs.get("tag", "-").title()
        return context

    def get_queryset(self) -> QuerySet[Post]:
        return self.queryset.filter(tags__slug=self.kwargs.get("tag"))


class PostDetailView(DetailView):
    queryset = Post.objects.prefetch_related("tags").published()
    context_object_name = "post"
    template_name = "blog/posts/detail.html"

    def get_template_names(self):
        if self.request.htmx:
            return ["blog/posts/detail.html#post-detail-content"]
        return [self.template_name]


class RelatedPostsView(ListView):
    template_name = "blog/posts/related_posts.html"
    context_object_name = "related_posts"
    paginate_by = 4

    def get_template_names(self):
        if self.request.htmx:
            return ["blog/posts/related_posts.html#related-posts-content"]
        return [self.template_name]

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


class ContactView(FormView):
    template_name = "blog/contact.html"
    form_class = ContactForm
    error_url = reverse_lazy("error")

    def get_template_names(self):
        if self.request.htmx:
            return ["blog/contact.html#contact-content"]
        return [self.template_name]

    def form_valid(self, form):
        context = {
            "name": form.cleaned_data["name"],
            "email": form.cleaned_data["email"],
            "message": form.cleaned_data["message"],
        }

        try:
            response = send_contact_message(**context)
            logger.info(response)
        except Exception:
            logger.exception("Contact problems")
            return redirect(self.error_url)

        return render(self.request, "blog/success.html", context)

    def form_invalid(self, form: ContactForm):
        # Use the same template for both HTMX and normal requests
        # The template will handle the conditional rendering based on request.htmx
        context_data = self.get_context_data(form=form)
        return render(self.request, self.template_name, context_data)
