from rest_framework import generics, filters, pagination, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from trucks.models import Truck, MenuItem
from .serializers import TruckSerializer, MenuItemSerializer


class TruckListView(generics.CreateAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = TruckSerializer

    def get_queryset(self):
        queryset = Account.objects.all()

        return queryset




class TruckDetailView(generics.RetrieveUpdateDestroyAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = TruckSerializer

    def get_queryset(self):
        return Truck.objects.all()


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.all()


class TruckViewSet(ModelViewSet):
    serializer_class = TruckSerializer
    queryset = Truck.objects.all()

    filter_fields = ('title')
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return Account.objects.all()


