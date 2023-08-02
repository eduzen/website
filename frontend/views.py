from django.http import HttpResponse
from django.views.generic import TemplateView

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
