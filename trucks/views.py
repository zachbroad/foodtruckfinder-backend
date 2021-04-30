import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseGone
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import DeleteView

from catering.models import CaterRequest
from onthegrub.mixins import FormSuccessMessageMixin
from .models import Truck, MenuItem, Review, TruckEvent, TruckFavorite


class TruckList(ListView):
    queryset = Truck.objects.all()
    paginate_by = 12
    template_name = 'trucks/trucks_list.html'
    context_object_name = 'trucks'

    def get_context_data(self, object_list=None, **kwargs):
        context = super(TruckList, self).get_context_data(**kwargs)
        los = [[truck.id, truck.title, [truck.lat, truck.lng]] for truck in Truck.objects.all()]
        context['truck_json'] = json.dumps(los)
        return context

    def get_queryset(self):
        if query := self.request.GET.get('query'):
            search_match_trucks = Truck.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(address__icontains=query)
            )
            return search_match_trucks

        return self.queryset


class FavoriteThisTruck(View, LoginRequiredMixin):
    model = TruckFavorite

    def get_object(self, request, *args, **kwargs):
        return self.model.objects.get(
            user=self.request.user,
            truck_id=self.kwargs.get('pk')
        )

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('trucks:detail', args=[self.kwargs.get('pk')]))

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        obj = self.model.objects.create(
            user=self.request.user,
            truck_id=self.kwargs.get('pk'),
        )

        # FIXME make cleaner
        truck = Truck.objects.get(id=self.kwargs.get('pk'))

        messages.info(request, f'{truck.title} added to favorites.')

        return HttpResponseRedirect(reverse_lazy('trucks:detail', args=[self.kwargs.get('pk')]))


class UnfavoriteThisTruck(DeleteView, LoginRequiredMixin):
    model = TruckFavorite

    def get_success_url(self):
        return reverse_lazy('trucks:detail', args=[self.kwargs.get('pk')])

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('trucks:detail', args=[self.kwargs.get('pk')]))

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        obj = self.model.objects.get(
            user=self.request.user,
            truck_id=self.kwargs.get('pk'),
        )
        obj.delete()

        # TODO: improve this  <><<><><>
        if obj:
            # FIXME make cleaner
            truck = Truck.objects.get(id=self.kwargs.get('pk'))
            messages.info(request, f'{truck.title} removed from favorites.')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseGone('You can\'t unfavorite this truck... you don\'t have it favorited!')


def detail(request, pk):
    truck = get_object_or_404(Truck, pk=pk)
    return render(request, 'trucks/truck_detail.html', {'truck': truck})


def menu(request, pk):
    full_menu = MenuItem.objects.filter(truck=pk)
    truck = Truck.objects.filter(id=pk).first()
    return render(request, 'trucks/truck_menu.html', {'menu': full_menu, 'truck': truck})


class MenuItemDetail(generic.DetailView):
    model = MenuItem
    pk_url_kwarg = 'item_id'
    context_object_name = 'item'


class BookCatering(generic.CreateView, FormSuccessMessageMixin):
    model = CaterRequest
    message = 'Cater request confirmed.'

    fields = [
        'name',
        'email',
        'phone',
        'details',
        'when',
        'duration',
    ]

    def get_context_data(self, **kwargs):
        context = super(BookCatering, self).get_context_data()
        context['truck'] = Truck.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.truck = Truck.objects.get(id=self.kwargs['pk'])
        FormSuccessMessageMixin.form_valid(self)
        return super().form_valid(form)

    def get_success_url(self):
        truck = Truck.objects.get(id=self.kwargs['pk'])
        return reverse('trucks:book-catering-success', kwargs={'pk': truck.id})


class BookCateringSuccess(TemplateView):
    template_name = 'trucks/truck_cater_booking_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['truck'] = Truck.objects.get(id=kwargs['pk'])
        return context


class TruckSchedule(generic.DetailView):
    model = Truck
    template_name_suffix = '_schedule'

    def get_object(self, queryset=None) -> Truck:
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['truck_events'] = self.get_object().schedule
        return context


class TruckEventDetail(generic.DetailView):
    model = TruckEvent
    context_object_name = 'event'

    def get_object(self, queryset=None) -> TruckEvent:
        return TruckEvent.objects.filter(truck_id=self.kwargs['pk'], id=self.kwargs['event_id']).first()


class ReviewList(generic.ListView):
    model = Review

    # paginate_by = 10 #TODO : FIX THE TEMPLATES SO THAT I CAN DO THIS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['truck'] = Truck.objects.filter(id=self.kwargs.get('pk')).first()
        return context

    def get_queryset(self):
        truck = Truck.objects.get(id=self.kwargs.get('pk'))
        return truck.reviews.all()


class ReviewCreate(generic.CreateView, LoginRequiredMixin):
    model = Review
    fields = [
        'rating',
        'description',
    ]

    def get_context_data(self, **kwargs):
        context = super(ReviewCreate, self).get_context_data(**kwargs)
        context['truck'] = Truck.objects.filter(id=self.kwargs.get('pk')).first()
        return context

    def form_valid(self, form):
        truck = Truck.objects.filter(id=self.kwargs.get('pk')).first()
        reviewer = self.request.user

        form.instance.truck = truck
        form.instance.reviewer = reviewer

        return super(ReviewCreate, self).form_valid(form)


class ReviewDetail(generic.DetailView):
    model = Review
    pk_url_kwarg = 'review_id'


class ReviewUpdate(generic.UpdateView):
    model = Review
