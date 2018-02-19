# -*- coding: utf-8 -*-
import logging
import requests
from collections import defaultdict
from datetime import datetime, timedelta, time

from django.http import HttpResponse
from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.shortcuts import redirect
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import WeekArchiveView
from django.views.generic.dates import DayArchiveView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic import ListView
from django.views.generic import TemplateView
from .models import Post, Comment
from .models import CustomPage, DolarPeso
from .forms import EmailForm
from .forms import CommentForm


logger = logging.getLogger('__name__')


class AboutView(TemplateView):
    template_name = "blog/about.html"


class ClasesView(TemplateView):
    template_name = "blog/clases.html"


class HomeListView(ListView):
    model = Post
    queryset = Post.objects.filter(published_date__isnull=False)
    context_object_name = 'posts'
    template_name = 'blog/body.html'
    ordering = ['-published_date', ]
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        tags = {}

        for post in self.queryset:
            for tag in post.tags.all():
                if tag.slug not in tags.keys():
                    tags[tag.slug] = {}
                    tags[tag.slug]['word'] = tag.word
                    tags[tag.slug]['size'] = 1
                else:
                    if tags[tag.slug]['size'] < 10:
                        tags[tag.slug]['size'] += 1

        context.update({
            'tags': tags,
        })
        return context


class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(published_date__isnull=False)
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'
    ordering = ['-published_date', ]
    paginate_by = 12


class PostTagsList(ListView):
    model = Post
    queryset = Post.objects.filter(published_date__isnull=False)
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'
    ordering = ['-published_date', ]
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(PostTagsList, self).get_context_data(**kwargs)
        tags = {}

        for post in self.queryset:
            for tag in post.tags.all():
                if tag.slug not in tags.keys():
                    tags[tag.slug] = {}
                    tags[tag.slug]['word'] = tag.word
                    tags[tag.slug]['size'] = 1
                else:
                    if tags[tag.slug]['size'] < 10:
                        tags[tag.slug]['size'] += 1

        context.update({
            'tags': tags,
            'tag': self.kwargs.get('tag').capitalize(),
        })
        return context

    def get_queryset(self):
        return self.queryset.filter(tags__slug=self.kwargs.get('tag'))


def stuff(request):
    # tweets = get_tweets(count=2)
    today = timezone.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    current_peso = DolarPeso.objects.filter(
        created_date__lte=today_end, created_date__gte=today_start
    )
    btc = requests.get('https://coinbin.org/btc')
    btc_data = defaultdict(str)
    if btc.status_code == requests.codes.ok:
        btc_data.update(btc.json()['coin'])

    if not current_peso.exists():
        # 'currency = 'Currency('ARS'")
        # end_date = "currency.data_set.get('DateTimeUTC'")
        # end_date = end_date.split(" ")
        # end_date[-1] = end_date[-1][:4]
        # end_date = " ".join(end_date)
        # date = datetime.strptime(end_date[:-1], '%Y-%m-%d %H:%M:%S %Z')
        data = {
            'name': "currency.data_set.get('Name')",
            'bid': "currency.data_set.get('Bid')",
            'ask': "currency.data_set.get('Ask')",
            'rate': "currency.data_set.get('Rate')",
            'created_date': timezone.now(),
        }
        # current_peso = DolarPeso.objects.create(**data)
    else:
        pass
        # current_peso = current_peso[0]

    data = {
        'tweet': 'tweets[0]',
        'name': "current_peso.name",
        'bid': "current_peso.bid",
        'ask': "current_peso.ask",
        'rate': "current_peso.rate",
        'date': "current_peso.created_date",
        'bdate': datetime.today(),
        'busd': btc_data['usd']
    }
    return render(request, 'blog/stuff.html', data)


def post_slug(request, slug):
    post = get_object_or_404(Post, slug=slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    related_posts = Post.objects.filter(
        published_date__isnull=False, tags__in=post.tags.all()).order_by(
            '-published_date').distinct().exclude(id=post.id)
    data = {
        'post': post,
        'related_posts': related_posts,
        'title': post.title,
    }
    return render(request, 'blog/post_detail.html', data)


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            email = EmailMessage(
                "Nuevo comment",
                form.cleaned_data.get('author'),
                form.cleaned_data.get('text'),
                "",
                ['eduardo.a.enriquez@gmail.com'],
            )
            email.send()
            logger.info("Email sent")
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


def custom_page(request, slug):
    custom_page = get_list_or_404(CustomPage, slug=slug)[0]

    data = {
        'title': custom_page.name,
        'custom_page': custom_page,
        'hide_navbar': not custom_page.include_header,
        'hide_footer': not custom_page.include_footer,
    }

    return render(request, 'blog/custom_page.html', data)


def contact(request):
    # tweets = get_tweets(count=2)

    if request.method == 'GET':
        contact_form = EmailForm()
        return render(request, 'blog/contact.html', {
            'form': contact_form, 'tweet': "tweets[0]",
        })

    if request.method == 'POST':
        contact_form = EmailForm(data=request.POST)

        if contact_form.is_valid():
            try:
                email = contact_form.cleaned_data.get('email')
                data = {
                    'name': contact_form.cleaned_data.get('name'),
                    'email': email,
                    'message': contact_form.cleaned_data.get('message'),
                }

                content = (
                    u"Hola, {name} escribio en la web contacto"
                    u"lo siguiente: {message} "
                    u" Si querés escribirle su mail es {email}"
                )

                email = EmailMessage(
                    "Nuevo contacto",
                    content.format(**data),
                    email,
                    ['eduardo.a.enriquez@gmail.com'],
                )
                email.send()
                logger.info("Email sent")

            except BadHeaderError:
                logger.exception("Email problems")
                return HttpResponse('Invalid header found.')

        contact_form = EmailForm()
        return render(request, 'blog/contact.html', {
            'form': contact_form, 'tweet': "tweets[0]",
        })


class PostMonthArchiveView(MonthArchiveView):
    queryset = Post.objects.all()
    date_field = "published_date"
    allow_future = True


class PostWeekArchiveView(WeekArchiveView):
    queryset = Post.objects.all()
    date_field = "published_date"
    week_format = "%W"
    allow_future = True


class PostDayArchiveView(DayArchiveView):
    queryset = Post.objects.all()
    date_field = "published_date"
    allow_future = True


class PostArchiveIndex(ArchiveIndexView):
    model = Post
    paginate_by = 50
    queryset = Post.objects.filter(published_date__isnull=False)
    template_name = 'blog/post_list.html'
    date_field = "published_date"
    allow_future = True
    context_object_name = 'posts'


def search_on_posts(request):
    results = Post.objects.filter(published_date__isnull=False,).order_by('-published_date')
    q = request.GET.get("q")
    if q:
        results = results.filter(Q(text_text__search=q), Q(title_text__search=q))

    data = {
        'posts': results,
        'tags': [],
        'python': False
    }
    return render(request, 'blog/bloglist.html', data)
