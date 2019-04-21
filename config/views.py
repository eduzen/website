from django.views.generic import TemplateView


class Google(TemplateView):
    template_name = "config/google.html"
