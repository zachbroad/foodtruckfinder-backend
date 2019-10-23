from rest_framework import serializers
from trucks.models import Truck, MenuItem


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ['pk',
                  'title',
                  'image',
                  'description',
                  ]
        read_only_fields = ['pk']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['name',
                  'description',
                  'price',
                  'image',
                  ]

