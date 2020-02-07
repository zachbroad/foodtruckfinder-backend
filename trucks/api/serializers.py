
from rest_framework import serializers
from users.api.serializers import AccountSerializer
from trucks.models import Truck, MenuItem, Menu, OpenningTime, Review
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
            'combos',
            'entres',
            'sides',
            'drinks',
            'deserts',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        reviewer = serializers.CurrentUserDefault()

        fields = [
            'pk',
            'reviewer',
            'rating',
            'description',
            'likes',
            'dislikes',
            'post_created',
            'post_edited',
        ]


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
            'phone',
            'website',
            'menu',
            'hours_of_operation',
            'tags',
            'reviews',
        ]
        read_only_fields = ['pk']
