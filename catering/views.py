from django.views.generic import ListView, DetailView

# Create your views here.
from trucks.models import Truck
from .models import CaterRequest


class CaterList(ListView):
    model = Truck

    def get_queryset(self):
        return Truck.objects.filter(available_for_catering=True)


class TruckCaterRequestList(ListView):
    model = CaterRequest

class CaterDetail(DetailView):
    model = CaterRequest
