from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, UpdateView, DetailView

# Create your views here.
from catering.models import CaterRequest
from notifications.models import Notification
from trucks.models import Truck, Visit


def get_db_context(self, context):
    context['my_trucks'] = self.request.user.trucks
    context['catering'] = self.request.user.my_cater_requests
    context['favorite_count'] = self.request.user.truck_favorites
    context['truck_views'] = Visit.owner_visits(self.request.user)
    return context


class DashboardIndex(TemplateView, LoginRequiredMixin):
    template_name = 'dashboard/dashboard_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_db_context(self, context)
        return context


class DashboardCateringIndex(ListView, LoginRequiredMixin):
    template_name = 'dashboard/dashboard_catering_index.html'
    queryset = Truck.objects.all()


class DashboardMyTrucksList(ListView, LoginRequiredMixin):
    template_name = 'dashboard/dashboard_trucks_list.html'
    queryset = Truck.objects.all()
    context_object_name = 'my_trucks'

    def get_queryset(self):
        user_trucks: QuerySet[Truck] = self.request.user.trucks

        if q := self.request.GET.get('query'):
            user_trucks = user_trucks.filter(Q(title__icontains=q) | Q(description__icontains=q))
            return user_trucks
        else:
            return user_trucks


class DashboardTruckDetail(DetailView, LoginRequiredMixin):
    template_name = 'dashboard/dashboard_detail.html'
    queryset = Truck.objects.all()
    pk_url_kwarg = 'truck_id'
    context_object_name = 'truck'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        truck: Truck = self.get_object()
        context['catering'] = truck.cater_requests
        context['favorite_count'] = truck.favorites.count
        context['truck_views'] = truck.visit_count
        return context


class DashboardEditTruck(UpdateView, LoginRequiredMixin):
    template_name = 'dashboard/dashboard_edit_truck.html'
    pk_url_kwarg = 'truck_id'
    queryset = Truck.objects.all()
    success_url = reverse_lazy('dashboard:truck-list')
    context_object_name = 'truck'
    fields = [
        'title',
        'description',
        'phone',
        'website',
        'tags',
        'available_for_catering',
    ]

    def form_valid(self, form):
        pass

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class DashboardNotifications(ListView, LoginRequiredMixin):
    template_name = 'dashboard/dashboard_notifications.html'
    queryset = Notification.objects.all()
    context_object_name = 'notifications'

    def get_queryset(self):
        pass
