from rest_framework import generics, filters, pagination
from rest_framework.viewsets import ModelViewSet

from trucks.models import Truck, MenuItem
from .serializers import TruckSerializer, MenuItemSerializer





class TruckListView(generics.CreateAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = TruckSerializer

    def get_queryset(self):
        queryset = Truck.objects.all()
        title = self.request.query_params.get('title')

        
        if title is not None:
            queryset = queryset.filter(title=title)


        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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

    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    pagination_class = pagination.LimitOffsetPagination
