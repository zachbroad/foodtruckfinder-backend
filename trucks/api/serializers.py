from rest_framework import serializers
from users.api.serializers import AccountSerializer
from trucks.models import Truck, MenuItem, OpenningTime, Review
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
    menu = MenuItemSerializer(many=True, required=False)
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
    menu = MenuItemSerializer(many=True, required=False)
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
