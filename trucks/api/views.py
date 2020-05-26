from django.utils import timezone
from django.db.models import Q, F, Count
from rest_framework import generics, pagination, permissions
from rest_framework import filters as drf_filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework import views
from trucks.models import Truck, Live, MenuItem, Review, Like, Visit, Tag
from users.models import FavoriteTruck
from .serializers import TruckSerializer, MenuItemSerializer, CreateTruckSerializer, ReviewSerializer, LikeSerializer, \
    VisitSerializer, TruckDashboardSerializer, CreateReviewSerializer, CreateMenuItemSerializer, TagSerializer,\
    PatchMenuItemSerializer, LiveSerializer


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.all()


class MenuItemViewSet(ModelViewSet):
    lookup_field = 'pk'
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()

    filterset_fields = ['truck', 'type', 'name', 'price']

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return PatchMenuItemSerializer
        if self.action == 'create':
            return CreateMenuItemSerializer
        return super().get_serializer_class()


class VisitViewSet(ModelViewSet):
    lookup_field = 'pk'
    serializer_class = VisitSerializer
    queryset = Visit.objects.all()

    filterset_fields = ['truck', 'visitor']


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    filterset_fields = ['truck', 'reviewer']

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateReviewSerializer

        if self.action == 'like':
            return LikeSerializer

        return super().get_serializer_class()

    @action(detail=True, methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'],
            permission_classes=(permissions.IsAuthenticated,))
    def like(self, request, pk=None):
        serializer = LikeSerializer(data=self.request.data, context={'request', self.request})

        if serializer.is_valid():
            existing_like = Like.objects.filter(liked_by=self.request.user)\
                .filter(review_id=pk)
            if existing_like.exists():
                obj: Like = existing_like.first()
                obj.is_liked = serializer.data['is_liked']
                ls = LikeSerializer(obj)
                return Response(ls.data)
            else:
                l = Like.objects.create(**serializer.data, liked_by=self.request.user, review_id=pk)
                ls = LikeSerializer(l)
                return Response(ls.data)

        else:
            return Response("Invalid data for LikeSerializer")


# TODO only allow owner to go live and within x miles/feet
class LiveViewSet(ModelViewSet):
    serializer_class = LiveSerializer
    queryset = Live.objects.all()
    permissions = permissions.IsAuthenticated

    filterset_fields = ['truck']


class TruckLiveViewSet(views.APIView):
    serializer_class = LiveSerializer
    queryset = Live.objects.all()
    permissions = permissions.IsAuthenticated

    def get(self, request, *args, **kwargs):
        serializer = LiveSerializer
        try:
            live = Live.objects.get((Q(start_time__lte=timezone.now(), end_time__gte=timezone.now()) &
                                     Q(truck__id=self.kwargs['truck'])))
            data = serializer(live, many=False, context={'request': request}, partial=True)
            data.save()
        except Live.DoesNotExist:
            raise ValidationError('Truck currently not live')

    def partial_update(self, request, *args, **kwargs):
        # TODO PATCH
        serializer = LiveSerializer
        try:
            live = Live.objects.get((Q(start_time__lte=timezone.now(), end_time__gte=timezone.now()) &
                                     Q(truck__id=self.kwargs['truck'])))
            if request.user.pk == live.truck.owner:
                data = serializer(live, many=False, context={'request': request}, partial=True)
                data.is_valid(raise_exception=True)
                data.save()
        except Live.DoesNotExist:
            raise ValidationError('You are not live')

        return Response(data.data)


class TruckViewSet(ModelViewSet):
    serializer_class = TruckSerializer
    queryset = Truck.objects.all()

    filter_backends = (drf_filters.SearchFilter,)
    search_fields = ('title',)
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        qs = super().get_queryset()

        title_contains = self.request.query_params.get('title__contains', None)
        owner = self.request.query_params.get('owner', None)

        geolocation = self.request.query_params.get('geolocation', None)
        MAX_DISTANCE = self.request.query_params.get('distance', 25)

        if geolocation is not None and self.action == 'list':
            lat, lng = geolocation.split(',')
            sorted_trucks = list()

            for truck in qs:
                dist = truck.distance(lat, lng)
                if dist <= float(MAX_DISTANCE):
                    sorted_trucks.append(truck)

            qs = sorted(sorted_trucks, key=lambda i: i.distance(lat, lng))
            return qs

        if title_contains is not None:
            q = Q()
            q = q | Q(title__contains=title_contains)
            qs = Truck.objects.filter(q).all()

        # if tags is not None:
        #     tags = tags.split(',')
        #     q = Q()
        #     for tag in tags:
        #         q = q | Q(tags__name__iexact=tag)
        #
        #     qs = Truck.objects.filter(q).all()

        if owner is not None:
            q = Q()
            q = q | Q(owner__pk=int(owner))

            qs = Truck.objects.filter(q).all()

        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTruckSerializer

        return TruckSerializer

    @action(detail=False, methods=["GET"])
    def trending(self, request):
        qs = self.get_queryset().annotate(favorite_count=Count(F('favorites'))).order_by('-favorite_count')
        serializer = self.get_serializer_class()
        data = serializer(qs, many=True, context={'request': request})
        return Response(data.data)

    @action(detail=False, methods=["GET"], permission_classes=[permissions.IsAuthenticated, ])
    def recent(self, request):
        qs = self.get_queryset()
        visits = Visit.objects.filter(visitor=self.request.user)[:10]
        qs = qs.filter(visits__in=visits).distinct()
        serializer = self.get_serializer_class()
        data = serializer(qs, many=True, context={'request': request})
        return Response(data.data)

    @action(detail=False, methods=["GET"], permission_classes=[permissions.IsAuthenticated, ])
    def favorites(self, request):
        qs = self.get_queryset()
        favorites = FavoriteTruck.objects.filter(user=self.request.user)
        qs = qs.filter(favorites__in=favorites)
        serializer = self.get_serializer_class()
        data = serializer(qs, many=True, context={'request': request})
        return Response(data.data)


class HomePage(views.APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        trucks = Truck.objects.all()

        trending = trucks.annotate(favorite_count=Count(F('favorites'))).order_by('-favorite_count')

        # User's recent
        visits = Visit.objects.filter(visitor=self.request.user)[:10]
        recent = trucks.filter(visits__in=visits).distinct()

        # Favorites
        favorites = FavoriteTruck.objects.filter(user=self.request.user)
        favorites = trucks.filter(favorites__in=favorites)

        # There's gotta be a better way to do this lmao
        ts_trending = TruckSerializer(trending, many=True, context={'request': request})
        ts_recent = TruckSerializer(recent, many=True, context={'request': request})
        ts_favorites = TruckSerializer(favorites, many=True, context={'request': request})
        ts_new = TruckSerializer(trucks.order_by("-pk"), many=True, context={'request': request})

        return Response({
            "trending": ts_trending.data,
            "new": ts_new.data,
            "recent": ts_recent.data,
            "favorites": ts_favorites.data,
        })


class DashboardViewSet(ModelViewSet):
    serializer_class = TruckDashboardSerializer
    queryset = Truck.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(owner=user)


class TagsViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
