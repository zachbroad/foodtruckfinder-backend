from django.shortcuts import render
from django.core.mail import send_mail
from grubtrucks.settings.production import DEFAULT_TO_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


def registration(request, email):
    subject = 'Thank you for registering to ourn site'
    message = ' it means a lot bro'
    email_from = DEFAULT_TO_EMAIL
    host = EMAIL_HOST_USER
    password = EMAIL_HOST_PASSWORD
    recipient_list = ['brandongevat@gmail.com', email]

    send_mail(subject, message, email_from, recipient_list, host, password,)


def index(request):
    template = "index.html"
    context = {}
    return render(request, template, context)
