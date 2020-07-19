from allauth.account import views


class SignupView(views.SignupView):
    template_name = "signup.html"


class LoginView(views.LoginView):
    template_name = "login.html"


class LogoutView(views.LogoutView):
    template_name = "logout.html"
