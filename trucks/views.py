from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Truck, MenuItem, Review, TruckEvent


def index(request):
    all_trucks = Truck.objects.all()

    if query := request.GET.get('query'):
        all_trucks = Truck.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'trucks/trucks_index.html', {'all_trucks': all_trucks})


def detail(request, truck_id):
    truck = get_object_or_404(Truck, pk=truck_id)
    return render(request, 'trucks/truck_detail.html', {'truck': truck})


def menu(request, truck_id):
    full_menu = MenuItem.objects.filter(truck=truck_id)
    return render(request, 'trucks/truck_menu.html', {'full_menu': full_menu})


class TruckSchedule(generic.DetailView):
    model = Truck
    template_name = "trucks/truck_schedule.html"
    pk_url_kwarg = 'truck_id'

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
        return TruckEvent.objects.filter(truck_id=self.kwargs['truck_id'], id=self.kwargs['event_id']).first()


class ReviewList(generic.ListView):
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['truck'] = Truck.objects.filter(id=self.kwargs.get('truck_id')).first()
        return context


class ReviewCreate(generic.CreateView):
    model = Review
    fields = [
        'rating',
        'description',
    ]

    def get_context_data(self, **kwargs):
        context = super(ReviewCreate, self).get_context_data(**kwargs)
        context['truck'] = Truck.objects.filter(id=self.kwargs.get('truck_id')).first()
        return context

    def form_valid(self, form):
        truck = Truck.objects.filter(id=self.kwargs.get('truck_id')).first()
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
