from rest_framework import serializers
from users.api.serializers import AccountSerializer
from trucks.models import Truck, MenuItem, Menu, OpenningTime, Review, Like
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

class OpenningTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenningTime

        fields = [
            'weekday',
            'from_hour',
            'to_hour',
        ]


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
    

    combos  = MenuItemSerializer(many=True, required=False)
    entres  = MenuItemSerializer(many=True, required=False)
    sides   = MenuItemSerializer(many=True, required=False)
    drinks  = MenuItemSerializer(many=True, required=False)
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
    class Meta:
        model = Like
        liked_by = serializers.CurrentUserDefault()

        fields = [
            'pk',
            'is_liked',
            'liked_by',
        ]

class ReviewSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()


    class Meta:
        model = Review
        reviewer = serializers.CurrentUserDefault()


        fields = [
            'pk',
            'reviewer',
            'rating',
            'description',
            'total_likes',
            'post_created',
            'post_edited',
        ]
    def get_total_likes(self, obj):
        return obj.likes.all().filter(is_liked=True).count() - obj.likes.all().filter(is_liked=False).count()

class CreateTruckSerializer(TaggitSerializer, serializers.ModelSerializer):
    hours_of_operation = OpenningTimeSerializer(many=True, required=False)
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


class TruckSerializer(TaggitSerializer, serializers.ModelSerializer):
    hours_of_operation = OpenningTimeSerializer(many=True)
    menu = MenuSerializer(many=True, required=False)
    owner = AccountSerializer()
    tags = TagListSerializerField()
    reviews = ReviewSerializer(many=True)

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
