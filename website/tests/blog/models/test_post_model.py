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


@pytest.mark.django_db
def test_create_post(superuser):
    post = Post.objects.create(
        title='My post1', slug='my-post1', text='Lorem ipsum1', author=superuser,
        published_date=datetime.now(), created_date=datetime.now())

    post_expected = Post.objects.get()
    assert post_expected
