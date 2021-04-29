import os

from django.core.mail import send_mail
from django.views.generic import TemplateView

from blog.models import ArticlePage
from trucks.models import Truck

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')


def registration(request, email):
    subject = 'Thank you for registering to ourn site'
    message = ' it means a lot bro'
    email_from = DEFAULT_FROM_EMAIL
    host = EMAIL_HOST_USER
    password = EMAIL_HOST_PASSWORD
    recipients = ['brandongevat@gmail.com', email]

    send_mail(subject, message, email_from, recipients, host, password, )


class IndexView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = ArticlePage.objects.all().live()
        context["trucks"] = Truck.get_trending()
        return context
