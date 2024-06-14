import logging
from typing import Any

from crispy_forms.helper import FormHelper  # type: ignore
from crispy_forms.layout import Field, Layout, Submit  # type: ignore
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext as _

from blog.services.captcha import verify_captcha

logger = logging.getLogger(__name__)

msg = _("Message")
email = _("Email")
name = _("Name")
captcha = _("What color is the red rabbit?")


class EmailForm(forms.Form):
    subject = forms.CharField(label="Nombre", max_length=100, required=True)
    from_email = forms.EmailField(max_length=150, label="E-mail", required=True)
    message = forms.CharField(label="Consulta", required=True, widget=forms.Textarea)

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

    def __str__(self):
        return f"<Form from {self.data}>"


class SearchForm(forms.Form):
    q = forms.CharField(label="", max_length=100, required=True)


class AdvanceSearchForm(forms.Form):
    q = forms.CharField(label="", max_length=100, required=True)


class ContactForm(forms.Form):
    name = forms.CharField(label=f"<span class='text-white'>{name}</span>")
    email = forms.EmailField(label=f"<span class='text-white'>{email}</span>")
    message = forms.CharField(label=f"<span class='text-white'>{msg}</span>", widget=forms.Textarea)
    captcha = forms.CharField(label=f"<span class='text-white'>{captcha}</span>")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name", css_class="mt-1 p-2 w-full rounded-md text-gray-800"),
            Field("email", css_class="mt-1 p-2 w-full rounded-md text-gray-800"),
            Field("message", css_class="mt-1 p-2 w-full resize rounded-md text-gray-800", rows=6),
            Field("captcha", css_class="mt-1 p-2 w-full rounded-md text-gray-800"),
            Submit("submit", _("Send"), css_class="px-4 py-2 bg-purple-500 rounded hover:bg-pink-300"),
        )

    def clean_captcha(self) -> str:
        # Get the cleaned value (after built-in validation checks)
        captcha = self.cleaned_data.get("captcha", "")
        if not verify_captcha(captcha):
            raise forms.ValidationError("invalid captcha")
        return captcha
