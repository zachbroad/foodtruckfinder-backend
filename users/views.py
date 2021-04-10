from allauth.account import views as allauth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, CreateView

from trucks.models import Truck
from users.models import User, UserReportModel


class UserDetail(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserList(ListView, LoginRequiredMixin):
    model = User


class UserTrucks(ListView, LoginRequiredMixin):
    model = Truck
    template_name = "user_truck_list.html"

    def get_queryset(self):
        user = User.objects.filter(username=self.kwargs['username']).first()
        return Truck.objects.filter(owner=user)

    def get_context_data(self, object_list=None, **kwargs):
        user = User.objects.filter(username=self.kwargs['username']).first()
        context = super().get_context_data(**kwargs)
        context['user'] = user
        return context


class ReportUser(CreateView):
    queryset = UserReportModel.objects.all()
    template_name = "users/report_user.html"
    fields = [
        'description',
    ]

    # def post(self, request, *args, **kwargs):
    #     desc = request.POST.get('description')
    #     user = User.objects.filter(username=kwargs.get('username'))

    # def dispatch(self, request, *args, **kwargs):
    #     self.

    def form_valid(self, form):
        return super(ReportUser, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.filter(username=self.kwargs['username']).first()
        return context


class SignupView(allauth_views.SignupView):
    template_name = "signup.html"
    success_url = reverse_lazy("grub-success")


class LoginView(allauth_views.LoginView):
    template_name = "login.html"


class LogoutView(allauth_views.LogoutView):
    template_name = "logout.html"


class SuccessView(TemplateView):
    template_name = "success.html"
