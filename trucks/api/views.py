# Generic --> Convienence

from rest_framework import generics
from trucks.models import Truck, MenuItem
from .serializers import TruckSerializer, MenuItemSerializer


class TruckAPIView(generics.CreateAPIView): # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = TruckSerializer

    def get_queryset(self):
        return Truck.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TruckRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = TruckSerializer

    def get_queryset(self):
        return Truck.objects.all()


class MenuItemRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.all()