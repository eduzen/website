from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("classes/", views.ClassesView.as_view(), name="classes"),
    path("search/", views.AdvanceSearch.as_view(), name="search"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("post/", views.PostListView.as_view(), name="post_list"),
    path("post/<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path("blog/", views.PostListView.as_view(), name="blog"),
    path("blog/<slug:slug>/", views.PostDetail.as_view(), name="blog_slug"),
    path("tags/<str:tag>/", views.PostTagsList.as_view(), name="bytag"),
    path("sucess/", views.SucessView.as_view(), name="sucess"),
    path("error/", views.ErrorView.as_view(), name="error"),
    path("consultancy", views.ConsultancyView.as_view(), name="consultancy"),
    path("language-dropdown/", views.language_dropdown, name="language_dropdown"),
]
