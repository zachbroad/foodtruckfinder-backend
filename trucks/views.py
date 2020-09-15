from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Truck, MenuItem, Review


def index(request):
    all_trucks = Truck.objects.all()
    return render(request, 'trucks/trucks_index.html', {'all_trucks': all_trucks})


def detail(request, truck_id):
    truck = get_object_or_404(Truck, pk=truck_id)
    return render(request, 'trucks/detail.html', {'truck': truck})


def menu(request, truck_id):
    full_menu = MenuItem.objects.filter(truck=truck_id)
    return render(request, 'trucks/menu.html', {'full_menu': full_menu})


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

class ReviewUpdate(generic.UpdateView):
    model = Review
