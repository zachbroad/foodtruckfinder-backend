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
    menu = MenuItemSerializer(many=True, required=False)
    owner = serializers.CurrentUserDefault()

    class Meta:
        model = Truck
        fields = [
            'pk',
            'owner',
            'title',
            'image',
            'description',
            'menu',
        ]
        read_only_fields = ['pk']
