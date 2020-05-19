import logging

from django.contrib.postgres.search import SearchVector
from django.shortcuts import redirect
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.dates import ArchiveIndexView, DayArchiveView, MonthArchiveView, WeekArchiveView

from .forms import AdvanceSearchForm, EmailForm, SearchForm
from .models import Post

logger = logging.getLogger(__name__)


class AboutView(TemplateView):
    template_name = "blog/about.html"


class ClasesView(TemplateView):
    template_name = "blog/clases.html"


class SucessView(TemplateView):
    template_name = "blog/success.html"


class ErrorView(TemplateView):
    template_name = "blog/error.html"


class AdvanceSearch(FormView):
    template_name = "blog/advance_search.html"
    form_class = AdvanceSearchForm
    success_url = "/sucess/"


class HomeListView(ListView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/home.html"
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
    template_name = "blog/home.html"
    ordering = ["-published_date"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Post.objects.count_tags()
        context["search_form"] = SearchForm()
        context["tag"] = self.kwargs.get("tag").title()
        return context

    def get_queryset(self):
        return self.queryset.filter(tags__slug=self.kwargs.get("tag"))


class PostDetail(DetailView):
    queryset = Post.objects.prefetch_related("tags").published()
    context_object_name = "post"

    def get_context_data(self, **kwargs):
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
    template_name = "blog/home.html"
    date_field = "published_date"
    allow_future = True
    context_object_name = "posts"
