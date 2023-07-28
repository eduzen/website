from django.views.generic import TemplateView

# Create your views here.


class BaseView(TemplateView):
    template_name = "frontend/base.html"


class ContactView(TemplateView):
    template_name = "frontend/contact.html"


class AboutView(TemplateView):
    template_name = "frontend/about.html"
