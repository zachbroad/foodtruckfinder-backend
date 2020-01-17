from rest_framework import generics, filters, pagination
from rest_framework.viewsets import ModelViewSet

from trucks.models import Truck, MenuItem
from .serializers import TruckSerializer, MenuItemSerializer


class TruckListView(generics.CreateAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = TruckSerializer

    def get_queryset(self):
        queryset = Account.objects.all()
        title = self.request.query_params.get('title')
        tags = self.request.query_params.get('tags')

        
        if title is not None:
            queryset = queryset.filter(title=title)
        elif tags:
            queryset = queryset.filter(tags=tags)

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
    search_fields = ('title', 'description', 'tags')
    pagination_class = pagination.LimitOffsetPagination


