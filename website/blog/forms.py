# -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from nocaptcha_recaptcha.fields import NoReCaptchaField

from .models import Comment


class EmailForm(forms.Form):
    name = forms.CharField(
        label=u"Nombre",
        max_length=100,
        required=True
    )
    email = forms.EmailField(
        max_length=150,
        label=u"E-mail",
        required=True,
    )
    message = forms.CharField(
        label=u"Consulta",
        required=True,
        widget=forms.Textarea
    )
    captcha = NoReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(
            Submit('submit', 'Enviar', css_class="btn-block", style="")
        )
        self.helper.form_tag = True
        self.helper.form_action = "/contact"


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
