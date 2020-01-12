import os
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView



class SignUpView(CreateView):
    success_url = reverse_lazy('login')
    template_name = os.path.join(settings.BASE_DIR, 'templates\\account\\signup.html')

class LoginView(CreateView):
    success_url = reverse_lazy('index')
    template_name = os.path.join(settings.BASE_DIR, 'templates\\account\\login.html')

