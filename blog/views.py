import logging

from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views.generic import FormView, ListView, TemplateView
from django.views.generic.dates import ArchiveIndexView, DayArchiveView, MonthArchiveView, WeekArchiveView

from .forms import AdvanceSearchForm, EmailForm, SearchForm
from .models import CustomPage, Post

logger = logging.getLogger(__name__)


class AboutView(TemplateView):
    template_name = "blog/about.html"


class ClasesView(TemplateView):
    template_name = "blog/clases.html"


class SucessView(TemplateView):
    template_name = "blog/success.html"


class StuffView(TemplateView):
    template_name = "blog/stuff.html"


class ErrorView(TemplateView):
    template_name = "blog/error.html"


class AdvanceSearch(FormView):
    template_name = "blog/advance_search.html"
    form_class = AdvanceSearchForm
    success_url = "/sucess/"


class HomeListView(ListView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/body.html"
    ordering = ["-published_date"]
    paginate_by = 12

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["tags"] = Post.objects.count_tags()
        context["search_form"] = SearchForm()
        return context


class PostListView(ListView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    ordering = ["-published_date"]
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if not query:
            return queryset

        return queryset.annotate(search=SearchVector("text", "title", "pompadour")).filter(search=query)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm()
        context["tags"] = Post.objects.count_tags()
        context["tag"] = self.request.GET.get("q", "")
        return context

    def render_to_response(self, context):
        posts = context.get("posts")
        if not posts:
            return redirect("search")

        return super().render_to_response(context)


class PostTagsList(ListView):
    model = Post
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    ordering = ["-published_date"]
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Post.objects.count_tags()
        context["search_form"] = SearchForm()
        context["tag"] = self.kwargs.get("tag").lower()
        return context

    def get_queryset(self):
        return self.queryset.filter(tags__slug=self.kwargs.get("tag"))


def post_slug(request, slug):
    post = get_object_or_404(Post, slug=slug)

    return render(request, "blog/post_detail.html", {"post": post})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    related_posts = (
        Post.objects.published()
        .filter(tags__in=post.tags.all())
        .order_by("-published_date")
        .distinct()
        .exclude(id=post.id)
    )
    data = {"post": post, "related_posts": related_posts, "title": post.title}
    return render(request, "blog/post_detail.html", data)


def custom_page(request, slug):
    custom_page = get_list_or_404(CustomPage, slug=slug)[0]

    data = {
        "title": custom_page.name,
        "custom_page": custom_page,
        "hide_navbar": not custom_page.include_header,
        "hide_footer": not custom_page.include_footer,
    }

    return render(request, "blog/custom_page.html", data)


class ContactView(FormView):
    template_name = "blog/contact.html"
    form_class = EmailForm
    success_url = "/sucess/"

    def form_valid(self, form):
        try:
            form.send_email()
            return super().form_valid(form)
        except Exception:
            logger.exception("Email problems")

        return redirect("/error/")


class PostMonthArchiveView(MonthArchiveView):
    queryset = Post.objects.published()
    date_field = "published_date"
    allow_future = True


class PostWeekArchiveView(WeekArchiveView):
    queryset = Post.objects.published()
    date_field = "published_date"
    week_format = "%W"
    allow_future = True


class PostDayArchiveView(DayArchiveView):
    queryset = Post.objects.published()
    date_field = "published_date"
    allow_future = True


class PostArchiveIndex(ArchiveIndexView):
    model = Post
    paginate_by = 50
    queryset = Post.objects.published()
    template_name = "blog/post_list.html"
    date_field = "published_date"
    allow_future = True
    context_object_name = "posts"
