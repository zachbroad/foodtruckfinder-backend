from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
from django.http.response import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, CreateView, DeleteView

# Create your views here.
from catering.models import CaterRequest
from notifications.models import Notification
from trucks.models import Truck, Visit, MenuItem


def get_db_context(self, context):
    context['my_trucks'] = self.request.user.trucks
    context['catering'] = self.request.user.my_cater_requests
    context['favorite_count'] = self.request.user.truck_favorites
    context['truck_views'] = Visit.owner_visits(self.request.user)
    return context


class DashboardIndex(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_db_context(self, context)
        return context


class DashboardCateringIndex(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_catering_index.html'
    queryset = CaterRequest.objects.all()


class DashboardCateringDetail(LoginRequiredMixin, DetailView):
    queryset = CaterRequest.objects.all()


class DashboardCaterRequestResponse(LoginRequiredMixin, UpdateView):
    queryset = CaterRequest.objects.all()
    success_url = reverse_lazy('dashboard:catering-index')
    fields = (
        'status',
    )


class DashboardMyTrucksList(LoginRequiredMixin, ListView):
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


class DashboardTruckDetail(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/dashboard_detail.html'
    queryset = Truck.objects.all()
    context_object_name = 'truck'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        truck: Truck = self.get_object()
        context['catering'] = truck.cater_requests
        context['favorite_count'] = truck.favorites.count
        context['truck_views'] = truck.visit_count
        return context


class DashboardEditTruck(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/dashboard_edit_truck.html'
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

    # def form_valid(self, form):
    #     pass

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class DashboardCreateItem(LoginRequiredMixin, CreateView):
    model = MenuItem
    context_object_name = 'item'
    fields = [
        'type',
        'name',
        'description',
        'price',
        'image',
        'featured',
    ]

    def get_success_url(self):
        return reverse_lazy('dashboard:view-menu', args=[self.kwargs['pk']])

    def form_valid(self, form):
        form.instance.truck = Truck.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)


class DashboardViewTruckMenu(LoginRequiredMixin, ListView):
    model = MenuItem
    context_object_name = 'items'

    def get_context_data(self, object_list=None, **kwargs):
        context = super(DashboardViewTruckMenu, self).get_context_data(**kwargs)
        context['truck'] = Truck.objects.get(id=self.kwargs.get('pk'))
        return context

    def dispatch(self, request, *args, **kwargs):
        if Truck.objects.get(id=self.kwargs.get('pk')).owner != self.request.user:
            return HttpResponseForbidden("You don't own this truck!")

        return super(DashboardViewTruckMenu, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return MenuItem.objects.filter(truck_id=self.kwargs.get('pk'), truck__owner=self.request.user)


class DashboardDeleteMenuItem(LoginRequiredMixin, DeleteView):
    model = MenuItem
    pk_url_kwarg = 'item_id'
    context_object_name = 'item'

    def get_success_url(self):
        return reverse_lazy('dashboard:view-menu', args=[self.kwargs['pk']])


class DashboardEditMenuItem(LoginRequiredMixin, UpdateView):
    model = MenuItem
    context_object_name = 'item'
    pk_url_kwarg = 'item_id'
    fields = [
        'type',
        'name',
        'description',
        'price',
        'image',
        'featured',
    ]

    def get_success_url(self):
        return reverse_lazy('dashboard:view-menu', args=[self.kwargs['pk']])


class DashboardViewTruckMenuItem(LoginRequiredMixin, DetailView):
    model = MenuItem
    context_object_name = 'item'
    template_name_suffix = '_detail_dashboard'
    pk_url_kwarg = 'item_id'

    def get_context_data(self, object_list=None, **kwargs):
        context = super(DashboardViewTruckMenuItem, self).get_context_data(**kwargs)
        context['truck'] = Truck.objects.get(id=self.kwargs.get('pk'))
        return context


class DashboardEditTruckMenu(LoginRequiredMixin, UpdateView):
    pass


class DashboardNotifications(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard_notifications.html'
    queryset = Notification.objects.all()
    context_object_name = 'notifications'

    def get_queryset(self):
        pass
