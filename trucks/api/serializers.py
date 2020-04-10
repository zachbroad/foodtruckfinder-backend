from django.db.models import Avg
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from trucks.models import Truck, MenuItem, Menu, OpenningTime, Review, Like, Visit
from users.api.serializers import AccountSerializer


class OpeningTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenningTime

        fields = [
            'weekday',
            'from_hour',
            'to_hour',
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
            'type',
            'name',
            'description',
            'price',
            'image',

        ]


class CreateMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem

        fields = [
            'truck',
            'type',
            'name',
            'description',
            'price',
            'image',

        ]


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
        model = Like

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
    reviewer = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review

        fields = [
            'truck',
            'reviewer',
            'rating',
            'description',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    truck = ReviewTruckSerializer()
    reviewer = AccountSerializer()
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


from grubtrucks.util import Base64ImageField


class CreateTruckSerializer(TaggitSerializer, serializers.ModelSerializer):
    menu = CreateMenuSerializer(many=True, required=False)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = TagListSerializerField()
    image = Base64ImageField(
        max_length=None, use_url=True, required=False, allow_empty_file=False, allow_null=True
    )

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
            'tags',
        ]
        read_only_fields = ['pk']

        def create(self, validated_data):
            menu_data = validated_data.pop('menu')

            truck = Truck.objects.create(**validated_data)

            for data in menu_data:
                menu_item = MenuItem.objects.create(truck=truck, **data)


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


class TruckSerializer(TaggitSerializer, serializers.ModelSerializer):
    hours_of_operation = OpeningTimeSerializer(many=True)
    menu = MenuSerializer(many=True, required=False)
    # visit_history = VisitSerializer(many=True, required=False)
    owner = serializers.CurrentUserDefault()
    tags = TagListSerializerField(allow_null=True, required=False)
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
            # 'visit_history',
            'hours_of_operation',
            'tags',
            'rating',
            'reviews',
            'favorites',
        ]
        read_only_fields = ['pk']

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
        rating = Review.objects.filter(truck=instance).all().aggregate(Avg('rating'))['rating__avg']
        if rating is not None:
            return rating


class TruckDashboardSerializer(TruckSerializer):
    visits = serializers.SerializerMethodField()

    class Meta:
        model = Truck
        fields = (
            'pk',
            'title',
            'image',
            'description',
            'address',
            'geolocation',
            'phone',
            'website',
            'menu',
            # 'visit_history',
            'hours_of_operation',
            'tags',
            'rating',
            'reviews',
            'favorites',
            'visits',
        )

        read_only_fields = (
            'pk',
            'visits',
            'reviews',
            'favorites',
        )

    def get_visits(self, instance):
        return instance.visits.count()
