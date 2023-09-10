from django.urls import path

from . import views

urlpatterns = [
    path("language-dropdown/", views.language_dropdown, name="language_dropdown"),
    path("chatgpt_improve_post/<int:post_id>/", views.chatgpt_improve_post, name="chatgpt_improve_post"),
]
