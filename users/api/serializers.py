from rest_framework import serializers
from users.models import Account, SearchTerm, FavoriteTruck
from trucks.api.serializers import TruckSerializer


class FavoriteTruckSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()

    truck = TruckSerializer(many=False, required=False)

    class Meta:
        model = FavoriteTruck
        fields = (
            'pk',
            'user',
            'truck',
        )


class SearchTermSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()

    class Meta:
        model = SearchTerm
        fields = (
            'user',
            'term',
            'created'
        )


class AccountSerializer(serializers.ModelSerializer):
    search_history = SearchTermSerializer(many=True, required=False)
    favorite_trucks = FavoriteTruckSerializer(many=True, required=False)

    class Meta:
        model = Account
        fields = (
            'pk',
            'username',
            'email',
            'phone',
            'first_name',
            'last_name',
            'search_history',
            'favorite_trucks'

        )
        read_only_fields = ['pk']
