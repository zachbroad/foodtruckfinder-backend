from django.db.models import Avg
from rest_framework import serializers
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


class CreateTruckSerializer(TaggitSerializer, serializers.ModelSerializer):
    hours_of_operation = OpeningTimeSerializer(many=True, required=False)
    menu = MenuSerializer(many=True, required=False)
    reviews = ReviewSerializer(many=True, required=False)
    owner = serializers.CurrentUserDefault()
    tags = TagListSerializerField()

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
            'hours_of_operation',
            'tags',
            'reviews',
        ]
        read_only_fields = ['pk']

        def to_internal_value(self, data):
            from django.core.files.base import ContentFile
            import base64
            import six
            import uuid

            # Check if this is a base64 string
            if isinstance(data, six.string_types):
                # Check if the base64 string is in the "data:" format
                if 'data:' in data and ';base64,' in data:
                    # Break out the header from the base64 content
                    header, data = data.split(';base64,')

                # Try to decode the file. Return validation error if it fails.
                try:
                    decoded_file = base64.b64decode(data)
                except TypeError:
                    self.fail('invalid_image')

                # Generate file name:
                file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
                # Get the file name extension:
                file_extension = self.get_file_extension(file_name, decoded_file)

                complete_file_name = "%s.%s" % (file_name, file_extension,)

                data = ContentFile(decoded_file, name=complete_file_name)

            return super(Base64ImageField, self).to_internal_value(data)

        def get_file_extension(self, file_name, decoded_file):
            import imghdr

            extension = imghdr.what(file_name, decoded_file)
            extension = "jpg" if extension == "jpeg" else extension

            return extension


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
