from django.views.generic import ListView, DetailView, CreateView

# Create your views here.
from trucks.models import Truck
from .models import CaterRequest


class CaterList(ListView):
    model = Truck
    paginate_by = 10

    def get_queryset(self):
        return Truck.objects.filter(available_for_catering=True)


class TruckCaterRequestList(ListView):
    model = CaterRequest


class CaterDetail(DetailView):
    model = CaterRequest


