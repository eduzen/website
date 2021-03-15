# import pytest
# from django.contrib.auth.models import User
# from hypothesis import given
# from hypothesis import strategies as st
# from hypothesis.extra.django import TestCase, from_model

# from blog.models import Post, Tag


# class DataCollectorTestCase(TestCase):
#     @given(from_model(Post, author=from_model(User), text=st.text(), slug=st.text(), title=st.text(min_size=10)))
#     def test_published_post(self, post):
#         assert Post.objects.filter(pk=post.pk).exists()

# @given(from_model(Tag))
# def test_create_tag(self, tag):
#     assert Tag.objects.filter(pk=tag.pk).exists()

# @pytest.mark.django_db(transaction=True)
# @given(from_model(Post, author=from_model(User), text=st.text(), slug=st.text()))
# def test_create_post(self, post):
#     assert Post.objects.filter(pk=post.pk).exists()
