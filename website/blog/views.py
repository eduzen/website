# -*- coding: utf-8 -*-
import logging
from yahoo_finance import Currency

from django.http import HttpResponse
from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required

from .twitter_api import get_tweets

from .models import Post, Comment
from .models import CustomPage
from .forms import EmailForm
from .forms import CommentForm


logger = logging.getLogger('__name__')


def home(request):
    posts = Post.objects.filter(
        published_date__isnull=False).order_by('-published_date')[:10]

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
    currency = Currency('ARS')
    data = {
        'tweet': tweets[0],
        'name': currency.data_set.get('Name'),
        'bid': currency.data_set.get('Bid'),
        'ask': currency.data_set.get('Ask'),
        'rate': currency.data_set.get('Rate'),
        'date': currency.data_set.get('Date'),
    }
    return render(request, 'blog/stuff.html', data)


def post_list(request):
    posts = Post.objects.filter(
        published_date__isnull=False).order_by('-published_date')

    data = {'posts': posts}

    return render(request, 'blog/post_list.html', data)


def post_slug(request, slug):
    post = get_object_or_404(Post, slug=slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
    })


def post_list_by_tag(request, tag):
    posts = Post.objects.filter(
        published_date__isnull=False, tags__word=tag).order_by(
        '-published_date')

    tags = [tg.word for post in posts for tg in post.tags.all()]

    data = {'posts': posts, 'tags': tags}

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
                    'phone': contact_form.cleaned_data.get('message'),
                }

                content = (
                    u"Hola, {name} escribio en la web lo siguiente: {message} <br/>"
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
