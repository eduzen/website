# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

from .models import Post
from .models import CustomPage


def home(request):
    posts = Post.objects.filter(
        published_date__isnull=False).order_by('-published_date')[:3]

    data = {
        'posts': posts,
    }
    return render(request, 'blog/body.html', data)


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

    data = {'posts': posts}

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


def custom_page(request, slug):
    custom_page = get_list_or_404(CustomPage, slug=slug)[0]

    data = {
        'title': custom_page.name,
        'custom_page': custom_page,
        'hide_navbar': not custom_page.include_header,
        'hide_footer': not custom_page.include_footer,
    }

    return render(request, 'blog/custom_page.html', data)
