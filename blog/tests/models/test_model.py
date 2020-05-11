from datetime import datetime

import pytest
from django.contrib.auth.models import User

from blog.tests.factories.post import PostFactory


@pytest.fixture()
def superuser():
    user = User.objects.create_superuser("myuser", "myemail@test.com", "pswd")
    return user


@pytest.mark.django_db
def test_post(superuser):
    post = PostFactory.create(author=superuser, published_date=datetime.now())
    assert post
