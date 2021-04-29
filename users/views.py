from allauth.account import views as allauth_views
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView

from trucks.models import Truck, Review
from users.models import User, UserReportModel


class UserDetail(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserList(ListView, LoginRequiredMixin):
    model = User


class UserTrucks(ListView, LoginRequiredMixin):
    model = Truck
    template_name = "users/user_truck_list.html"

    def get_queryset(self):
        user = User.objects.filter(username=self.kwargs['username']).first()
        return Truck.objects.filter(owner=user)

    def get_context_data(self, object_list=None, **kwargs):
        user = User.objects.filter(username=self.kwargs['username']).first()
        context = super().get_context_data(**kwargs)
        context['user'] = user
        return context


class UserFavorites(ListView, LoginRequiredMixin):
    model = Truck
    template_name = "users/user_truck_list_favorite.html"

    def get_queryset(self):
        user = User.objects.filter(username=self.kwargs['username']).first()
        return Truck.objects.filter(owner=user, favorites__in=user.my_favorite_trucks)

    def get_context_data(self, object_list=None, **kwargs):
        user = User.objects.filter(username=self.kwargs['username']).first()
        context = super().get_context_data(**kwargs)
        context['user'] = user
        return context


class UserReviews(ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = 'users/user_reviews.html'

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs.get('username'))
        if not user:
            return None

        return user.reviews

    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs.get('username'))
        if not user:
            return HttpResponseNotFound('No user found with that name.')

        return super(UserReviews, self).dispatch(request)


class UserEditProfile(UpdateView):
    model = User
    fields = [
        'email',
        'first_name',
        'last_name',
        'phone',
        'biography',
    ]
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/user_edit.html'

    def form_valid(self, form):
        messages.success(self.request, 'Successfully saved profile.')
        return HttpResponseRedirect(self.get_success_url())

    # def dispatch(self, request, *args, **kwargs):
    #     messages.success(self.request, self.get_success_message(self))
    #     return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:detail', args=[self.request.user])


class ReportUser(CreateView):
    queryset = UserReportModel.objects.all()
    template_name = "users/report_user.html"
    fields = [
        'description',
    ]

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
