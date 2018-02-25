import pytest
from datetime import datetime
from django.test import Client

from blog.models import Post

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


@pytest.fixture()
def client():
    return Client()


@pytest.fixture()
def posts():
    user = User.objects.create_superuser('myuser', 'myemail@test.com', 'pswd')
    post0 = Post(
        title='My post1', slug='my-post1', text='Lorem ipsum1', author=user,
        published_date=datetime.now(), created_date=datetime.now())
    post0.save()

    post1 = Post(
        title='My post2', slug='my-post2', text='Lorem ipsum2', author=user,
        published_date=datetime.now(), created_date=datetime.now())
    post1.save()

    post2 = Post(
        title='My post3', slug='my-post3', text='Lorem ipsum3', author=user,
        published_date=datetime.now(), created_date=datetime.now())
    post2.save()

    return [post0, post1, post2]


@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_post(client, posts):
    post = posts[0]
    response = client.get(reverse('post_detail', kwargs={"pk": post.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_post_list(client, posts):
    response = client.get(reverse('post_list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_about(client, posts):
    response = client.get(reverse('about'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_bad_about(client, posts):
    response = client.get('wp/admin')
    assert response.status_code == 404
