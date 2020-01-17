from rest_framework import serializers

from trucks.models import Truck, MenuItem
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem

        fields = [
            'name',
            'description',
            'price',
            'image',
        ]


class TruckSerializer(TaggitSerializer, serializers.ModelSerializer):
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
            'tags',
        ]
        read_only_fields = ['pk']
