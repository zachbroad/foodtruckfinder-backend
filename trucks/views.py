from django.shortcuts import render, get_object_or_404

from trucks.api.serializers import TruckSerializer, MenuItemSerializer
from .models import Truck, MenuItem


def index(request):
    all_trucks = Truck.objects.all()
    return render(request, 'trucks/index.html', {'all_trucks': all_trucks})


def detail(request, truck_id):
    truck = get_object_or_404(Truck, pk=truck_id)
    return render(request, 'trucks/detail.html', {'truck': truck})


def menu(request, truck_id):

    full_menu = MenuItem.objects.filter(truck=truck_id)
    return render(request, 'trucks/menu.html', {'full_menu': full_menu})


