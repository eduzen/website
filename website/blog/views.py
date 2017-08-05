# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta, time
from yahoo_finance import Currency

from django.http import HttpResponse
from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import WeekArchiveView
from django.views.generic.dates import DayArchiveView

from .twitter_api import get_tweets

from .models import Post, Comment
from .models import CustomPage, DolarPeso
from .forms import EmailForm
from .forms import CommentForm


logger = logging.getLogger('__name__')


def home(request):
    posts_list = Post.objects.filter(
        published_date__isnull=False).order_by('-published_date')

    paginator = Paginator(posts_list, 12)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    tweets = get_tweets(count=2)

    data = {
        'posts': posts,
        'tweet': tweets[0],
    }
    return render(request, 'blog/body.html', data)


def bio(request):
    tweets = get_tweets(count=2)
    data = {
        'tweet': tweets[0],
    }
    return render(request, 'blog/bio.html', data)


def stuff(request):
    tweets = get_tweets(count=2)
    # import pdb; pdb.set_trace()
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    current_peso = DolarPeso.objects.filter(
        created_date__lte=today_end, created_date__gte=today_start
    )
    if not current_peso.exists():
        currency = Currency('ARS')
        end_date = currency.data_set.get('DateTimeUTC')
        end_date = end_date.split(" ")
        end_date[-1] = end_date[-1][:4]
        end_date = " ".join(end_date)
        date = datetime.strptime(end_date[:-1], '%Y-%m-%d %H:%M:%S %Z')
        data = {
            'name': currency.data_set.get('Name'),
            'bid': currency.data_set.get('Bid'),
            'ask': currency.data_set.get('Ask'),
            'rate': currency.data_set.get('Rate'),
            'created_date': date,
        }
        current_peso = DolarPeso.objects.create(**data)
    else:
        current_peso = current_peso[0]

    data = {
        'tweet': tweets[0],
        'name': current_peso.name,
        'bid': current_peso.bid,
        'ask': current_peso.ask,
        'rate': current_peso.rate,
        'date': current_peso.created_date,
    }
    return render(request, 'blog/stuff.html', data)


def post_list(request):
    posts_list = Post.objects.filter(
        published_date__isnull=False).order_by('-published_date')

    paginator = Paginator(posts_list, 12)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    data = {'posts': posts}

    return render(request, 'blog/post_list.html', data)


def post_slug(request, slug):
    post = get_object_or_404(Post, slug=slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
    })


def post_list_by_tag(request, tag):
    posts_list = Post.objects.filter(
        published_date__isnull=False, tags__word=tag).order_by(
        '-published_date')

    paginator = Paginator(posts_list, 12)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    python = tag == u'python'
    tags = {}
    for post in posts_list:
        for tag in post.tags.all():
            if tag.slug not in tags.keys():
                tags[tag.slug] = {}
                tags[tag.slug]['word'] = tag.word
                tags[tag.slug]['size'] = 1
            else:
                if tags[tag.slug]['size'] < 10:
                    tags[tag.slug]['size'] += 1

    data = {'posts': posts, 'tags': tags, 'python': python}
    return render(request, 'blog/post_list.html', data)


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
    tweets = get_tweets(count=2)

    if request.method == 'GET':
        contact_form = EmailForm()
        return render(request, 'blog/contact.html', {
            'form': contact_form, 'tweet': tweets[0],
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
                    u"Hola, {name} escribio en la web lo siguiente: {message} "
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
            'form': contact_form, 'tweet': tweets[0],
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


def clases(request):
    return render(request, 'blog/clases.html', )


def search_on_posts(request):
    q = request.GET.get("q")
    if q:
        results = Post.objects.filter(
            published_date__isnull=False,
            name__icontains=q).order_by('-published_date')
    else:
        results = Post.objects.filter(published_date__isnull=False).order_by('-published_date')

    data = {'posts': results, 'tags': [], 'python': False}
    return render(request, 'blog/post_list.html', data)
