import pytest
from django.contrib.auth.models import User
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.django import from_model

from blog.models import Post, Tag


@given(from_model(Tag))
def test_create_tag(db, tag):
    assert Tag.objects.filter(pk=tag.pk).exists()


@pytest.mark.django_db(transaction=True)
@given(from_model(Post, author=from_model(User), text=st.text(), slug=st.text()))
def test_create_post(post):
    assert Post.objects.filter(pk=post.pk).exists()


@given(from_model(Post, author=from_model(User), text=st.text(), slug=st.text()))
def test_published_post(db, post):
    post.publish()
    assert post in Post.objects.published()
