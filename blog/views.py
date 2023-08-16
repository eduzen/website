import datetime as dt
import logging
from typing import Any

from constance import config
from django import http
from django.contrib.postgres.search import SearchVector
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, FormView, ListView, TemplateView

from blog.services.contact import send_telegram_message

from .forms import AdvanceSearchForm, SearchForm
from .models import Post

logger = logging.getLogger(__name__)

MIN = 60
HOUR = 60 * MIN
DAY = 24 * HOUR
MONTH = 30 * DAY
HALF_YEAR = 6 * MONTH


class ConfigMixin:
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)  # type: ignore
        context["config"] = config
        return context


@method_decorator(cache_page(DAY), name="dispatch")
class AboutView(ConfigMixin, TemplateView):
    template_name = "blog/about.html"

    def get_context_data(self, **kwargs):
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
    template_name = "blog/advance_search.html"
    form_class = AdvanceSearchForm
    success_url = "/sucess/"


@method_decorator(cache_page(MONTH), name="dispatch")
class HomeView(TemplateView):
    template_name = "blog/home.html"


@method_decorator(cache_page(MONTH), name="dispatch")
class ConsultancyView(TemplateView):
    template_name = "blog/consultancy.html"


@method_decorator(cache_page(MONTH), name="dispatch")
class ClassesView(TemplateView):
    template_name = "blog/classes.html"


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
    template_name = "blog/posts/list.html"
    ordering = ["-published_date"]
    paginate_by = 12

    def get_queryset(self) -> QuerySet[Post]:
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if not query:
            return queryset  # type: ignore

        queryset = queryset.annotate(search=SearchVector("text", "title", "pompadour")).filter(  # type: ignore
            search=query
        )
        return queryset  # type: ignore

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm()
        context["tags"] = Post.objects.count_tags()
        context["tag"] = self.request.GET.get("q", "")
        return context

    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> http.HttpResponse:
        posts = context.get("posts")
        if not posts:
            return redirect("search")

        return super().render_to_response(context)


@method_decorator(cache_page(HOUR), name="dispatch")
class PostTagsList(ListView):
    model = Post
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/posts/list.html"
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
    template_name = "blog/posts/detail.html"

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
class ContactView(ConfigMixin, TemplateView):
    template_name = "blog/contact.html"
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
            response = send_telegram_message(f"Message from website {context}")
            logger.info(response)

            return render(request, "blog/success.html", context)

        except Exception:
            logger.exception("Contact problems")
            return redirect(self.error_url)


class Google(TemplateView):
    template_name = "blog/google.html"
