from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import TemplateView

from catering.models import CaterRequest
from onthegrub.mixins import FormSuccessMessageMixin
from .models import Truck, MenuItem, Review, TruckEvent


def index(request):
    all_trucks = Truck.objects.all()

    if query := request.GET.get('query'):
        all_trucks = Truck.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'trucks/trucks_list.html', {'all_trucks': all_trucks})


def detail(request, pk):
    truck = get_object_or_404(Truck, pk=pk)
    return render(request, 'trucks/truck_detail.html', {'truck': truck})


def menu(request, pk):
    full_menu = MenuItem.objects.filter(truck=pk)
    truck = Truck.objects.filter(id=pk).first()
    return render(request, 'trucks/truck_menu.html', {'menu': full_menu, 'truck': truck})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['truck'] = Truck.objects.filter(id=self.kwargs.get('pk')).first()
        return context


class ReviewCreate(generic.CreateView):
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


from django.views import View


# class ReviewCreateForm(ModelForm):
#     class Meta:
#         model = Review
#         fields = [
#             'rating',
#             'description',
#         ]


class ReviewListCreate(View):

    def get(self, request, *args, **kwargs):
        view = ReviewList.as_view()
        return view(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return HttpResponseForbidden()
    #
    #     # request.data
    #
    #     view = ReviewCreate.as_view()
    #     return view(request, *args, **kwargs)


class ReviewDetail(generic.DetailView):
    model = Review
    pk_url_kwarg = 'review_id'


class ReviewUpdate(generic.UpdateView):
    model = Review
