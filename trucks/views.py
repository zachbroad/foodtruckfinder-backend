from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render, get_object_or_404

from trucks.api.serializers import TruckSerializer, MenuItemSerializer
from .models import Truck, MenuItem


def index(request):
    all_trucks = Truck.objects.all()
    return render(request, 'trucks/index.html', {'all_trucks': all_trucks})


def detail(request, truck_id):
    truck = get_object_or_404(Truck, pk=truck_id)
    return render(request, 'trucks/detail.html', {'truck': truck})


class TruckViewSet(ModelViewSet):
    serializer_class = TruckSerializer
    queryset = Truck.objects.all()


class MenuItemViewSet(ModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
