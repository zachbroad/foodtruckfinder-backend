from allauth.account import views as allauth_views
from django.views.generic import DetailView, ListView

from users.models import User


class UserDetail(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserList(ListView):
    model = User


class SignupView(allauth_views.SignupView):
    template_name = "signup.html"


class LoginView(allauth_views.LoginView):
    template_name = "login.html"


class LogoutView(allauth_views.LogoutView):
    template_name = "logout.html"
