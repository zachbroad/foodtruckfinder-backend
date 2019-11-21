import os
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from rest_framework.viewsets import ModelViewSet
from users.api.serializers import AccountSerializer
from users.models import Account

class SignUpView(CreateView):
    success_url = reverse_lazy('login')
    template_name = os.path.join(settings.BASE_DIR, 'templates\\account\\signup.html')

class LoginView(CreateView):
    success_url = reverse_lazy('index')
    template_name = os.path.join(settings.BASE_DIR, 'templates\\account\\login.html')

class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
