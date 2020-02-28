from django.db.models import Q
from rest_framework import generics, pagination, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from trucks.models import Truck, MenuItem, Review, Like
from .serializers import TruckSerializer, MenuItemSerializer, CreateTruckSerializer, ReviewSerializer, LikeSerializer

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
        hlsearch|:echo
        
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


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'like':
            return LikeSerializer

        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'LIKE':
            return (permissions.IsAuthenticated,)

        return super().get_permissions()

    @action(detail=True, methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
    def like(self, request, pk=None):
        # data = list(self.request.data)
        # data['liked_by'] = self.request.user
        serializer = LikeSerializer(data=self.request.data, context={'request', self.request})

        if serializer.is_valid():
            existing_like = Like.objects.filter(liked_by=self.request.user, review_id=pk)
            if existing_like.exists():
                obj: Like = existing_like.first()
                obj.is_liked = serializer.data['is_liked']
                ls = LikeSerializer(obj)
                return Response(ls.data)
            else:
                l = Like.objects.create(**serializer.data, liked_by=self.request.user, review_id=pk)
                ls = LikeSerializer(l)
                return Response(ls.data)
                    # return Response("Unable to create Like... {}".format(serializer.error_messages))

        else:
            return Response("Invalid data for LikeSerializer")

class TruckViewSet(ModelViewSet):
    serializer_class = TruckSerializer
    queryset = Truck.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        qs = super().get_queryset()

        tags = self.request.query_params.get('tags', None)
        if tags is not None:
            tags = tags.split(',')
            q = Q()
            for tag in tags:
                q = q | Q(tags__name__iexact=tag)

            qs = Truck.objects.filter(q).all()

        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            q = Q()
            q = q | Q(owner__pk=int(owner))

            qs = Truck.objects.filter(q).all()

        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTruckSerializer

        return TruckSerializer
