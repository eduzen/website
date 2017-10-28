import pytest
from datetime import datetime
from django.test import Client
from blog.models import Post

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


@pytest.fixture()
def superuser():
    user = User.objects.create_superuser('myuser', 'myemail@test.com', 'pswd')
    return user


@pytest.fixture()
def post():
    user = User.objects.create_superuser('myuser', 'myemail@test.com', 'pswd')
    post = Post.objects.create(
        title='My post1', slug='my-post1', text='Lorem ipsum1', author=user,
        published_date=datetime.now(), created_date=datetime.now())
    return post


@pytest.mark.django_db
def test_create_post(superuser):
    post = Post.objects.create(
        title='My post1', slug='my-post1', text='Lorem ipsum1', author=superuser,
        published_date=datetime.now(), created_date=datetime.now())

    post_expected = Post.objects.get()
    assert post_expected


@pytest.mark.django_db
def test_modified_post(post):
    post = Post.objects.get(post.id)
    post.text = 'other text'
    post.save()

    post_expected = Post.objects.get(post.id)
    assert post_expected.text == 'other text'
