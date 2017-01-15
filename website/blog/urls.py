from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^custom/(?P<slug>[\w-]+)/$', views.custom_page, name='custom_page'),
    url(r'^blog/$', views.post_list, name='entries'),
    url(r'^blog/(?P<pk>[0-9]+)/$', views.post_detail, name='post'),
    url(r'^blog/(?P<slug>[\w-]+)/$', views.post_detail, name='post'),
    url(r'^blog/(?P<tag>[\w-]+)/$', views.post_list_by_tag, name='bytag'),
]
