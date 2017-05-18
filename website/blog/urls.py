from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^bio/$', views.bio, name='bio'),
    url(r'^about/$', views.bio, name='bio'),
    url(r'^custom/(?P<slug>[\w-]+)/$', views.custom_page, name='custom_page'),
    url(r'^blog/$', views.post_list, name='entries'),
    url(r'^blog/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^blog/(?P<slug>[\w-]+)/$', views.post_slug, name='post'),
    url(r'^tags/(?P<tag>[\w-]+)/$', views.post_list_by_tag, name='bytag'),
    url(
        r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post,
        name='add_comment'
    ),
    url(
        r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve,
        name='comment_approve'
    ),
    url(
        r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove,
        name='comment_remove'
    ),
]
