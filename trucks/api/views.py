import datetime

from dateutil import parser
from django.db.models import Q, F, Count
from django.utils import timezone
from rest_framework import filters as drf_filters
from rest_framework import generics, pagination, permissions, status
from rest_framework import views
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from trucks.models import Truck, Live, MenuItem, Review, ReviewLike, Visit, Tag, TruckEvent
from users.models import FavoriteTruck
from .serializers import TruckSerializer, MenuItemSerializer, CreateTruckSerializer, ReviewSerializer, LikeSerializer, \
    VisitSerializer, TruckDashboardSerializer, CreateReviewSerializer, CreateMenuItemSerializer, TagSerializer, \
    PatchMenuItemSerializer, LiveSerializer, TruckEventSerializer


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
            existing_like = ReviewLike.objects.filter(liked_by=self.request.user) \
                .filter(review_id=pk)
            if existing_like.exists():
                obj: ReviewLike = existing_like.first()
                obj.is_liked = serializer.data['is_liked']
                ls = LikeSerializer(obj)
                return Response(ls.data)
            else:
                l = ReviewLike.objects.create(**serializer.data, liked_by=self.request.user, review_id=pk)
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

    def create(self, validated_data):

        start_time = timezone.now()
        data = validated_data.data.copy()
        try:
            currently_live = Live.objects.get((Q(start_time__lte=timezone.now(), end_time__gte=timezone.now()) &
                                               Q(truck__id=data['truck'])))
            if currently_live.count() > 0:
                raise ValidationError('You are currently live')
        except Live.DoesNotExist:
            pass

        truck = Truck.objects.get(pk=data.pop('truck')[0])
        end_time = data.get('end_time', None)
        if end_time is not None:
            end_time = parser.parse(end_time)
            data.pop('end_time')
        else:
            end_time = start_time + datetime.timedelta(hours=1)
        live = Live.objects.create(truck=truck, end_time=end_time, **data)
        live.save()
        live_serialized = self.serializer_class(live)
        return Response(live_serialized.data)


class TruckLiveViewSet(generics.UpdateAPIView):
    serializer_class = LiveSerializer
    queryset = Live.objects.all()
    permissions = permissions.IsAuthenticated

    def get_object(self, *args, **kwargs):
        return Live.objects.get((Q(start_time__lte=timezone.now(), end_time__gte=timezone.now()) &
                                 Q(truck__id=self.kwargs['truck'])))

    def get(self, request, *args, **kwargs):
        serializer = LiveSerializer
        try:
            live = self.get_object()
            data = serializer(live, many=False, context={'request': request}, partial=True)
        except Live.DoesNotExist:
            raise ValidationError('Truck currently not live')
        return Response(data.data)

    # TODO if end_time is none set end_time to timezone.now()
    def partial_update(self, request, *args, **kwargs):
        data = request.data

        try:
            live = self.get_object()

            end_time = data.get('end_time', None)
            if end_time is not None:
                end_time = parser.parse(end_time)
                data.pop('end_time')
            else:
                end_time = timezone.now()

            live.end_time = end_time
            live.save()
        except Live.DoesNotExist:
            raise ValidationError('You are not live')
        serializer = LiveSerializer(live, many=False, context={'request': request}, partial=True)
        return Response(serializer.data)


class TruckViewSet(ModelViewSet):
    serializer_class = TruckSerializer
    queryset = Truck.objects.all()
    filter_backends = (drf_filters.SearchFilter,)
    search_fields = ('title',)
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        qs = super().get_queryset()

        tag_startswith = self.request.query_params.get('tags__title__startswith', None)
        title_startswith = self.request.query_params.get('title__startswith', None)
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

        if tag_startswith is not None:
            qs = (Truck.objects.filter(tags__title__startswith=tag_startswith).all())

        if title_startswith is not None:
            qs = Truck.objects.filter(title__startswith=title_startswith).all()

        if title_startswith is not None and tag_startswith is not None:
            q = Q(Q(title__startswith=title_startswith) | Q(tags__title__startswith=tag_startswith))
            qs = Truck.objects.filter(q)

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

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        tag_objs = []
        menu_objs = []

        try:
            truck = self.get_object()
            tags = data.get('tags', None)
            # title = data.get('title', None)
            # description = data.get('description', None)
            # menu = data.get('menu', None)
            # phone = data.get('phone', None)
            # website = data.get('website', None)
            # geolocation = data.get('geolocation', None)
            # catering = data.get('catering', None)

            if tags is not None:
                truck.tags.clear()
                for tag in tags:
                    tgobj = Tag.objects.filter(id=tag).first()
                    truck.tags.add(tgobj)

        except Truck.DoesNotExist:
            raise ValidationError('Truck doesn\'t exist')
        except Tag.DoesNotExist:
            raise ValidationError('Tag doesn\'t exist')
        except Exception as e:
            return Response("Error: {}".format(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = TruckSerializer(truck, many=False, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTruckSerializer
        if self.action == 'events':
            return TruckEventSerializer

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

    @action(detail=True, methods=["GET", "POST"], permission_classes=[permissions.AllowAny],
            serializer_class=TruckEventSerializer, )  # TODO perm changes
    def events(self, request, pk=None):
        if request.method == "GET":
            qs = self.get_queryset()
            events = list(TruckEvent.objects.filter(truck=self.get_object()).all())
            serializer = TruckEventSerializer(events, many=True, context={'request': request})
            return Response(serializer.data)

        if request.method == "POST":  # handle these perms better
            truck = Truck.objects.filter(id=pk).first()
            if truck.owner != request.user:
                return Response({"error": "You don't have permission to create events for this truck!"},
                                status=status.HTTP_401_UNAUTHORIZED)
            serializer = TruckEventSerializer(data=request.data, many=False, context={'request': request})
            serializer.is_valid(raise_exception=True)
            TruckEvent.objects.create(**serializer.data, truck_id=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        qs = Tag.objects.all()

        featured = self.request.query_params.get('featured', None)

        if featured is not None:
            qs = Tag.objects.filter(featured=featured).all()

        return qs
