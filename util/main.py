import os

from django.core.mail import send_mail

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')


def send_email(email):
    subject = 'Subject'
    message = 'Message'
    email_from = DEFAULT_FROM_EMAIL
    host = EMAIL_HOST_USER
    password = EMAIL_HOST_PASSWORD
    recipients = ['brandongevat@gmail.com', email]

    send_mail(subject, message, email_from, recipients, host, password, )
