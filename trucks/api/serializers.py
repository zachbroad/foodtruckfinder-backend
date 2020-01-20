from rest_framework import serializers

from users.api.serializers import AccountSerializer
from trucks.models import Truck, MenuItem, OpenningTime
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


class CreateTruckSerializer(TaggitSerializer, serializers.ModelSerializer):
    hours_of_operation = OpenningTimeSerializer(many=True)
    menu = MenuItemSerializer(many=True, required=False)
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
            'menu',
            'hours_of_operation',
            'tags',
        ]
        read_only_fields = ['pk']


class TruckSerializer(TaggitSerializer, serializers.ModelSerializer):
    hours_of_operation = OpenningTimeSerializer(many=True)
    menu = MenuItemSerializer(many=True, required=False)
    owner = AccountSerializer()
    tags = TagListSerializerField()

    class Meta:
        model = Truck
        fields = [
            'pk',
            'owner',
            'title',
            'image',
            'description',
            'menu',
            'hours_of_operation',
            'tags',
        ]
        read_only_fields = ['pk']
