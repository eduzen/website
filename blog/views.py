import logging
import requests
from collections import defaultdict
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.postgres.search import SearchVector
from django.views.generic.dates import (
    MonthArchiveView, WeekArchiveView, DayArchiveView, ArchiveIndexView
)
from django.views.generic import ListView, TemplateView, FormView
from .models import Post, CustomPage
from .forms import EmailForm, SearchForm, AdvanceSearchForm

logger = logging.getLogger(__name__)


class AboutView(TemplateView):
    template_name = "blog/about.html"


class ClasesView(TemplateView):
    template_name = "blog/clases.html"


class SucessView(TemplateView):
    template_name = "blog/success.html"


class ErrorView(TemplateView):
    template_name = "blog/error.html"


def _count_tags(slug, word, tags):
    if slug not in tags:
        tags[slug]["word"] = word
        tags[slug]["size"] = 1
        return

    if tags[slug]["size"] < 12:
        tags[slug]["size"] += 1


def _parse_post_tags(post, tags):
    for tag in post.tags.all():
        _count_tags(tag.slug, tag.word, tags)


class HomeListView(ListView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/body.html"
    ordering = ["-published_date"]
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Post.objects.count_tags()
        context["search_form"] = SearchForm()
        return context


class PostListView(ListView):
    model = Post
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    ordering = ["-published_date"]
    paginate_by = 12

    def get_queryset(self):
        query_set = super(PostListView, self).get_queryset()
        query = self.request.GET.get("q")
        if not query:
            return query_set

        return query_set.annotate(search=SearchVector("text", "title", "pompadour")).filter(search=query)

    def _count_tags(self, slug, word, tags):
        if slug not in tags:
            tags[slug]["word"] = word
            tags[slug]["size"] = 1
            return

        if tags[slug]["size"] < 12:
            tags[slug]["size"] += 1

    def _parse_post_tags(self, post, tags):
        for tag in post.tags.all():
            self._count_tags(tag.slug, tag.word, tags)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Post.objects.count_tags()

        query = self.request.GET.get("q")
        if not query:
            return context

        posts = context.get('posts')
        if not posts:
            return context

        tags = defaultdict(dict)
        for post in posts:
            _parse_post_tags(post, tags)

        search_form = SearchForm()
        context.update({"tags": dict(tags), "search_form": search_form, "tag": query})
        return context

    def render_to_response(self, context):
        posts = context.get('posts')
        if not posts:
            return redirect('search')

        return super(PostListView, self).render_to_response(context)


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


def get_coin_value(url):
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        return

    return response


def advance_search(request):
    advance_search_form = AdvanceSearchForm()
    data = {'advance_search_form': advance_search_form}
    return render(request, "blog/advance_search.html", data)


def stuff(request):
    data = {
        "tweet": "",
        "name": "",
        "bid": "",
        "ask": "",
        "rate": "",
        "date": "",
        "bdate": datetime.today(),
        "busd": "",
    }
    return render(request, "blog/stuff.html", data)


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
    success_url = '/sucess/'

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
