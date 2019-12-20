from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings, production


def email(request, email):
    subject = 'Thank you for registering to ourn site'
    message = ' it means a lot bro'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['brandongevat@gmail.com',]
    send_mail (subject, message, email_from, recipient_list)


def index(request):
    template = "index.html"
    context = {}
    return render(request, template, context)
