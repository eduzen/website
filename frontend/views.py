from typing import Any

from django.http import HttpResponse
from django.views.generic import ListView, TemplateView

from blog.forms import SearchForm
from blog.models import Post

# Create your views here.


class BaseView(TemplateView):
    template_name = "frontend/base.html"


class ContactView(TemplateView):
    template_name = "frontend/contact.html"

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return HttpResponse("<div class='text-center green'>Sent!</div>")


class AboutView(TemplateView):
    template_name = "frontend/about.html"


class ConsultancyView(TemplateView):
    template_name = "frontend/consultancy.html"


class HomeListView(ListView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    template_name = "frontend/posts/list.html"
    ordering = ["-published_date"]
    paginate_by = 12

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tags"] = Post.objects.count_tags()
        context["search_form"] = SearchForm()
        return context
