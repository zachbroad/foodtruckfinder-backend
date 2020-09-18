from datetime import timezone

from django.db.models import Avg
from django.db.models import Q
from rest_framework import serializers

from grubtrucks.util import Base64ImageField
from trucks.models import Truck, MenuItem, Menu, Review, ReviewLike, Visit, Tag, Live


class LiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        truck = serializers.SerializerMethodField()

        fields = [
            'truck',
            'start_time',
            'end_time',
            'live_time',
            'live'
        ]

    def truck(self, obj):
        return obj.pk

    def validate(self, data):
        if timezone.now() < data['end_time']:
            lives = Live.objects.filter(
                (Q(start_time__lte=self.end_time, end_time__gte=self.start_time)) & Q(truck__id=self.truck.pk))
            editing = lives[0].pk == self.pk
            if lives.exists() and not editing:
                raise serializers.ValidationError(
                    'You are already live, or will be live during this time')

            
            return data
        else:
            raise serializers.ValidationError(
                'Can not have end time before the start time')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag

        fields = [
            'pk',
            'title',
            'featured',
            'icon',
        ]


class VisitSerializer(serializers.ModelSerializer):
    visitor = serializers.CurrentUserDefault()
    truck = serializers.SerializerMethodField()

    class Meta:
        model = Visit

        fields = [
            'pk',
            'truck',
            'visitor',
            'visited'
        ]

    def truck(self, obj):
        return obj.pk


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem

        fields = [
            'pk',
            'type',
            'name',
            'description',
            'price',
            'image',
            'featured',
        ]


class PatchMenuItemSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None, use_url=True, required=False, allow_empty_file=False, allow_null=True
    )

    class Meta:
        model = MenuItem

        fields = [
            'pk',
            'type',
            'name',
            'description',
            'price',
            'image',
            'featured',
        ]


class CreateMenuItemSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None, use_url=True, required=False, allow_empty_file=False, allow_null=True
    )

    class Meta:
        model = MenuItem
        read_only_fields = ('pk',)

        fields = [
            'pk',
            'truck',
            'type',
            'name',
            'description',
            'price',
            'image',
            'featured',
        ]

    def create(self, validated_data):
        menu_item = MenuItem.objects.create(**validated_data)

        return menu_item


class CreateMenuSerializer(serializers.ModelSerializer):
    menu_items = CreateMenuItemSerializer(many=True, required=False)

    class Meta:
        model = MenuItem

        fields = [
            'menu_items'
        ]


class MenuSerializer(serializers.ModelSerializer):
    combos = MenuItemSerializer(many=True, required=False)
    entres = MenuItemSerializer(many=True, required=False)
    sides = MenuItemSerializer(many=True, required=False)
    drinks = MenuItemSerializer(many=True, required=False)
    deserts = MenuItemSerializer(many=True, required=False)

    class Meta:
        model = Menu

        fields = [
            'entres',
            'sides',
            'drinks',
            'deserts',
            'combos',
        ]


class LikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ReviewLike

        read_only_fields = (
            'pk',
        )

        fields = [
            'pk',
            'is_liked',
            'liked_by',
        ]


class ReviewTruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = [
            'pk',
            'title',
            'image',
        ]


class CreateReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.CurrentUserDefault()

    class Meta:
        model = Review

        fields = [
            'truck',
            'reviewer',
            'rating',
            'description',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class BasicAccountSerializer(serializers.ModelSerializer):
        class Meta:
            from users.models import User
            model = User
            fields = (
                'pk',
                'username',
                'first_name',
                'last_name',
            )
            read_only_fields = ['pk']

    total_likes = serializers.SerializerMethodField()
    truck = ReviewTruckSerializer()
    reviewer = BasicAccountSerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Review

        fields = [
            'id',
            'truck',
            'reviewer',
            'rating',
            'description',
            'total_likes',
            'post_created',
            'post_edited',
        ]

        read_only_fields = [
            'total_likes',
            'post_created',
            'post_edited',
        ]

    def get_total_likes(self, obj):
        return obj.likes.all().filter(is_liked=True).count() - obj.likes.all().filter(is_liked=False).count()


class CreateTruckSerializer(serializers.ModelSerializer):
    menu = CreateMenuSerializer(many=True, required=False)
    owner = serializers.CurrentUserDefault()
    image = Base64ImageField(
        max_length=None, use_url=True, required=False, allow_empty_file=False, allow_null=True
    )
    geolocation = serializers.CharField(required=False)

    class Meta:
        model = Truck
        fields = [
            'pk',
            'owner',
            'title',
            'image',
            'description',
            'address',
            'geolocation',
            'phone',
            'website',
            'menu',
            'available_for_catering',
        ]
        read_only_fields = ['pk', 'live']

    def create(self, validated_data):
        truck = Truck.objects.create(**validated_data)
        data = validated_data

        if data.__contains__('menu'):
            menu_data = data.pop('menu')
            for item in menu_data:
                MenuItem.objects.create(truck=truck, **item)
        return truck

        # def create(self, request, *args, **kwargs):
        #     is_many = isinstance(request.data, list)
        #     if not is_many:
        #         return super(TruckViewSet, self).create(request, *args, **kwargs)
        #     else:
        #         serializer = self.get_serializer(data=request.data, many=True)
        #         serializer.is_valid(raise_exception=True)
        #         self.perform_create(serializer)
        #         headers = self.get_success_headers(serializer.data)
        #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TruckSerializer(serializers.ModelSerializer):
    menu = MenuItemSerializer(many=True, required=False, source='items')
    # visit_history = VisitSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)
    owner = serializers.CurrentUserDefault()
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    favorites = serializers.IntegerField(source='num_favorites')

    class Meta:
        model = Truck
        fields = [
            'pk',
            'owner',
            'title',
            'image',
            'distance',
            'description',
            'address',
            'geolocation',
            'phone',
            'website',
            'menu',
            'tags',
            'rating',
            'reviews',
            'favorites',
            'live',
            'available_for_catering',
        ]
        read_only_fields = ['pk', 'rating', 'distance', 'live']

    def get_distance(self, instance):
        try:
            request = self.context['request']
            geo = request.query_params.get('geolocation', None)
            if geo is not None:
                geo = geo.split(',')
                return instance.distance(geo[0], geo[1])
        except:
            return None

        return None

    def get_rating(self, instance):
        rating = Review.objects.filter(truck=instance).all(
        ).aggregate(Avg('rating'))['rating__avg']
        if rating is not None:
            return rating




class TruckDashboardSerializer(TruckSerializer):
    menu = MenuItemSerializer(many=True, required=False, source='items')
    owner = serializers.CurrentUserDefault()
    visits = serializers.SerializerMethodField()

    class Meta:
        model = Truck
        fields = (
            'pk',
            'owner',
            'title',
            'image',
            'description',
            'address',
            'geolocation',
            'phone',
            'website',
            'menu',
            # 'visit_history',
            'tags',
            'rating',
            'reviews',
            'favorites',
            'visits',
            'live',
            'available_for_catering',
        )

        read_only_fields = (
            'pk',
            'visits',
            'reviews',
            'favorites',
        )

    def get_visits(self, instance):
        return instance.visits.count()
