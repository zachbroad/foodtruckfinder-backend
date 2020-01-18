from rest_framework import generics, filters, pagination
from rest_framework.viewsets import ModelViewSet

from trucks.models import Truck, MenuItem
from .serializers import TruckSerializer, MenuItemSerializer, CreateTruckSerializer


""" class TruckListView(generics.CreateAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = TruckSerializer

    def get_queryset(self):
        queryset = Truck.objects.all()
        title = self.request.query_params.get('title')
        tags = self.

        
        if title is not None:
            queryset = queryset.filter(title=title)


        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
 """

""" class TruckDetailView(generics.RetrieveUpdateDestroyAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = TruckSerializer

    def get_queryset(self):
      return Truck.objects.all() """


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

    def get_queryset(self):

        qs = super().get_queryset()

        tags=self.kwargs.get('tags', None)

        if tags is not None:
            tags = tags.split(',')
            tags = Tags.objects.filter(tags__name__in=tags)
            qs = Truck.objects.filter(tags__in=tags)

        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTruckSerializer

        return TruckSerializer

