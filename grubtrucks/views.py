from django.shortcuts import render
from django.core.mail import send_mail
from grubtrucks.settings.production import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL


def registration(request, email):
    subject = 'Thank you for registering to ourn site'
    message = ' it means a lot bro'
    email_from = DEFAULT_FROM_EMAIL
    host = EMAIL_HOST_USER
    password = EMAIL_HOST_PASSWORD
    recipients = ['brandongevat@gmail.com', email]

    send_mail(subject, message, email_from, recipients, host, password,)


def index(request):
    template = "index.html"
    context = {}
    return render(request, template, context)
