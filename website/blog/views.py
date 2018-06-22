# -*- coding: utf-8 -*-
import logging
import requests
from collections import defaultdict
from datetime import datetime
from django.http import HttpResponse
from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import WeekArchiveView
from django.views.generic.dates import DayArchiveView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic import ListView
from django.views.generic import TemplateView
from .models import Post, Comment
from .models import CustomPage
from .forms import EmailForm
from .forms import CommentForm
from .forms import SearchForm


logger = logging.getLogger("__name__")


class AboutView(TemplateView):
    template_name = "blog/about.html"


class ClasesView(TemplateView):
    template_name = "blog/clases.html"


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
    model = Post
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/body.html"
    ordering = ["-published_date"]
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        tags = defaultdict(dict)
        for post in self.queryset.prefetch_related("tags"):
            _parse_post_tags(post, tags)

        search_form = SearchForm()
        context.update({"tags": dict(tags), "search_form": search_form})
        return context


class PostListView(ListView):
    model = Post
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    ordering = ["-published_date"]
    paginate_by = 12

    def get_queryset(self):
        result = super(PostListView, self).get_queryset()
        query = self.request.GET.get("q")
        if query:
            result = result.annotate(search=SearchVector("text", "title", "pompadour")).filter(search=query)

        return result

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        tags = defaultdict(dict)
        for post in self.queryset.prefetch_related("tags"):
            _parse_post_tags(post, tags)

        search_form = SearchForm()
        context.update({"tags": dict(tags), "search_form": search_form, "tag": self.request.GET.get("q", "").lower()})
        return context


class PostTagsList(ListView):
    model = Post
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    ordering = ["-published_date"]
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(PostTagsList, self).get_context_data(**kwargs)
        tags = defaultdict(dict)

        for post in self.queryset.prefetch_related("tags"):
            _parse_post_tags(post, tags)

        search_form = SearchForm()

        context.update({"search_form": search_form, "tags": dict(tags), "tag": self.kwargs.get("tag").lower()})
        return context

    def get_queryset(self):
        return self.queryset.filter(tags__slug=self.kwargs.get("tag"))


def get_coin_value(url):
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        return

    return response


def stuff(request):
    btc = get_coin_value("https://coinbin.org/btc")
    if not btc:
        btc = get_coin_value("https://api.coindesk.com/v1/bpi/currentprice.json")

    try:
        btc = btc.json()["coin"]
    except Exception:
        btc = btc.json()["bpi"]["USD"]["rate"]

    data = {
        "tweet": "tweets[0]",
        "name": "current_peso.name",
        "bid": "current_peso.bid",
        "ask": "current_peso.ask",
        "rate": "current_peso.rate",
        "date": "current_peso.created_date",
        "bdate": datetime.today(),
        "busd": btc,
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


def contact(request):
    if request.method == "GET":
        contact_form = EmailForm()
        return render(request, "blog/contact.html", {"form": contact_form, "tweet": "tweets[0]"})

    if request.method == "POST":
        contact_form = EmailForm(data=request.POST)

        if contact_form.is_valid():
            try:
                email = contact_form.cleaned_data.get("email")
                data = {
                    "name": contact_form.cleaned_data.get("name"),
                    "email": email,
                    "message": contact_form.cleaned_data.get("message"),
                }

                content = (
                    "Hola, {name} escribio en la web contacto"
                    "lo siguiente: {message} "
                    " Si querés escribirle su mail es {email}"
                )

                email = EmailMessage("Nuevo contacto", content.format(**data), email, ["eduardo.a.enriquez@gmail.com"])
                email.send()
                logger.info("Email sent")

            except BadHeaderError:
                logger.exception("Email problems")
                return HttpResponse("Invalid header found.")

        contact_form = EmailForm()
        return render(request, "blog/contact.html", {"form": contact_form, "tweet": "tweets[0]"})


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
