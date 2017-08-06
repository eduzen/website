from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^bio/$', views.bio, name='about'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^stuff/$', views.stuff, name='stuff'),
    url(r'^util/$', views.stuff, name='stuff'),
    url(r'^clases/$', views.clases, name='clases'),
    url(r'^contactar/$', views.contact, name='contact'),
    url(r'^contacto/$', views.contact, name='contact'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^custom/(?P<slug>[\w-]+)/$', views.custom_page, name='custom_page'),
    url(r'^blog/$', views.post_list, name='entries'),
    url(r'^blog/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^blog/(?P<slug>[\w-]+)/$', views.post_slug, name='post_slug'),
    url(r'^tags/(?P<tag>[\w-]+)/$', views.post_list_by_tag, name='bytag'),
    url(r'^post/$', views.PostListView.as_view(), name='post_list'),
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
    # Example: /2012/aug/
    url(
        r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',
        views.PostMonthArchiveView.as_view(),
        name="archive_month"
    ),
    # Example: /2012/08/
    url(
        r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        views.PostMonthArchiveView.as_view(month_format='%m'),
        name="archive_month_numeric"
    ),
    # Example: /2012/week/23/
    url(
        r'^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$',
        views.PostWeekArchiveView.as_view(),
        name="archive_week"
    ),
    # Example: /2012/nov/10/
    url(
        r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/$',
        views.PostDayArchiveView.as_view(),
        name="archive_day"
    ),
]
