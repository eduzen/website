import logging

from captcha.fields import CaptchaField
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger("blog.views")


class EmailForm(forms.Form):
    subject = forms.CharField(label="Nombre", max_length=100, required=True)
    from_email = forms.EmailField(max_length=150, label="E-mail", required=True)
    message = forms.CharField(label="Consulta", required=True, widget=forms.Textarea)
    captcha = CaptchaField()

    def _prepare_data(self):
        data = {}
        data["subject"] = f"{self.data['subject']} Nuevo contacto a traves de la eduzen.com.ar"
        data["recipient_list"] = ["eduardo.a.enriquez@gmail.com"]
        data["message"] = self.data["message"]
        data["html_message"] = (
            f"<html><body><p>eduzen.com.ar<p><hr/><p>{self.data['subject']} - {self.data['from_email']}</p>"
            f"<hr/><p>{self.data['message']}</p></body></html>"
        )
        data["from_email"] = settings.DEFAULT_FROM_EMAIL
        return data

    def send_email(self):
        data = self._prepare_data()
        send_mail(**data)
        logger.info(f"{data} sent to me")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Enviar", css_class="btn-block", style=""))
        self.helper.form_tag = True
        self.helper.form_action = "/contact/"

    def __str__(self):
        return f"<Form from {self.data}>"


class SearchForm(forms.Form):
    q = forms.CharField(label="", max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "navbar-form"
        self.helper.form_tag = True
        self.helper.layout = Layout(
            AppendedText(
                "q",
                (
                    '<i class="fa fa-search" onclick='
                    "\"document.getElementsByClassName('navbar-form')[0].submit()\">"
                    "</i>"
                ),
            )
        )
        self.helper.form_action = "/post/"
        self.helper.form_method = "GET"


class AdvanceSearchForm(forms.Form):
    q = forms.CharField(label="", max_length=100, required=True)
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.layout = Layout(
            AppendedText(
                "q",
                (
                    '<i class="fa fa-search" onclick='
                    "\"document.getElementsByClassName('form-inline')[0].submit()\">"
                    "</i>"
                ),
            )
        )
        self.helper.add_input(Submit("submit", "Buscar", css_class="btn-block", style=""))
        self.helper.form_action = "/post/"
        self.helper.form_method = "GET"
