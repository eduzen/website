import pytest
from datetime import datetime
from django.test import Client

from blog.models import Post

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_home_view():
    client = Client()
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_post():
    client = Client()
    user = User.objects.create_superuser('myuser', 'myemail@test.com', 'pswd')

    post = Post.objects.create(
        title='My post', slug='my-post', text='Lorem ipsum', author=user,
        published_date=datetime.now(), created_date=datetime.now())

    response = client.get(reverse('post_detail', kwargs={"pk": post.id}))

    assert response.status_code == 200

