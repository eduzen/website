import datetime as dt
import logging
from typing import Any

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, FormView, TemplateView
from django_filters.views import FilterView

from .filters import PostFilter
from .forms import AdvanceSearchForm
from .models import Post
from .services.telegram import send_message

logger = logging.getLogger(__name__)

MIN = 60
HOUR = 60 * MIN
DAY = 24 * HOUR
MONTH = 30 * DAY
HALF_YEAR = 6 * MONTH


class HtmxGetMixin:
    partial_template_name: str

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.htmx and self.partial_template_name:  # type: ignore
            self.template_name = self.partial_template_name
        return super().get(request, *args, **kwargs)  # type: ignore


@method_decorator(cache_page(DAY), name="dispatch")
class AboutView(HtmxGetMixin, TemplateView):
    template_name = "blog/about.html"
    partial_template_name = "blog/partials/about.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        start_year = 2014
        current_year = dt.datetime.now().year
        context["years_of_experience"] = current_year - start_year
        return context


@method_decorator(cache_page(DAY), name="dispatch")
class SucessView(TemplateView):
    template_name = "blog/success.html"


@method_decorator(cache_page(DAY), name="dispatch")
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


@method_decorator(cache_page(HOUR), name="dispatch")
class PostListView(HtmxGetMixin, FilterView):
    queryset = Post.objects.published().prefetch_related("tags")
    context_object_name = "posts"
    template_name = "blog/posts/list.html"
    partial_template_name = "blog/partials/posts/list.html"
    ordering = ["-published_date"]
    filterset_class = PostFilter
    paginate_by = 12


@method_decorator(cache_page(HOUR), name="dispatch")
class PostTagsListView(HtmxGetMixin, FilterView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/posts/list.html"
    partial_template_name = "blog/partials/posts/list.html"
    ordering = ["-published_date"]
    filterset_class = PostFilter
    paginate_by = 12

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("tag", "-").title()
        return context

    def get_queryset(self) -> QuerySet[Post]:
        return self.queryset.filter(tags__slug=self.kwargs.get("tag"))


@method_decorator(cache_page(DAY), name="dispatch")
class PostDetailView(DetailView):
    queryset = Post.objects.prefetch_related("tags").published()
    context_object_name = "post"
    template_name = "blog/posts/detail.html"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Get all tag IDs for the current post
        tag_ids = self.object.tags.values_list("id", flat=True)

        related_posts = (
            Post.objects.published()
            .filter(tags__id__in=tag_ids)
            .order_by("-published_date")
            .distinct()
            .exclude(pk=self.object.pk)
        )
        # Pagination logic for related posts
        paginator = Paginator(related_posts, 4)
        page = self.request.GET.get("related_page", 1)
        context["related_posts"] = paginator.get_page(page)

        return context


@method_decorator(cache_page(DAY), name="get")
class ContactView(HtmxGetMixin, TemplateView):
    template_name = "blog/contact.html"
    partial_template_name = "blog/partials/contact.html"
    error_url = reverse_lazy("error")
    success_url = reverse_lazy("success")

    def verify_captcha(self, request: HttpRequest) -> bool:
        user_answer = request.POST.get("captcha_response", None)
        correct_answer = ("rojo", "red")
        if user_answer and user_answer.strip().lower() in correct_answer:
            return True
        return False

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not self.verify_captcha(request):
            return render(request, "blog/error.html", {"error": _("invalid captcha")})

        context = {}
        if name := request.POST.get("name"):
            context["name"] = name

        if email := request.POST.get("email"):
            context["email"] = email

        if message := request.POST.get("message"):
            context["message"] = message

        try:
            # Send a test message
            response = send_message(f"Message from website {context}")
            logger.info(response)

            return render(request, "blog/success.html", context)

        except Exception:
            logger.exception("Contact problems")
            return redirect(self.error_url)


@cache_page(HALF_YEAR)
def language_dropdown(request):
    return render(request, "blog/utils/language_dropdown.html")
