from rest_framework import serializers

from trucks.models import Truck, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem

        fields = [
            'name',
            'description',
            'price',
            'image',
        ]


class TruckSerializer(serializers.ModelSerializer):
    menu = MenuItemSerializer(many=True)

    class Meta:
        model = Truck
        fields = [
            'pk',
            'title',
            'title',
            'image',
            'description',
            'menu',
        ]
        read_only_fields = ['pk']
