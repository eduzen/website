from django.conf import settings
from blog.forms import EmailForm


def test_mail(mailoutbox):
    data = {
        'subject': "Turanga Leela",
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'message': "Hi there",
    }
    email_form = EmailForm(data)
    email_form.send_email()

    assert len(mailoutbox) == 1
