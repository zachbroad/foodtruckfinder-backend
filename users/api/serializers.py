from rest_framework import serializers

from users.models import User, SearchTerm, FavoriteTruck, Feedback


class FavoriteTruckSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()

    class Meta:
        model = FavoriteTruck
        fields = (
            'pk',
            'user',
            'truck',
        )


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()

    class Meta:
        model = Feedback
        fields = (
            'pk',
            'user',
            'image',
            'description',
        )


class SearchTermSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()

    class Meta:
        model = SearchTerm
        fields = (
            'user',
            'term',
            'searched_on'
        )


class UserSerializer(serializers.ModelSerializer):
    from trucks.api.serializers import TruckSerializer
    search_history = SearchTermSerializer(many=True, required=False)
    favorite_trucks = FavoriteTruckSerializer(many=True, required=False)
    trucks = TruckSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'email',
            'phone',
            'first_name',
            'last_name',
            'search_history',
            'trucks',
            'favorite_trucks'
        )
        read_only_fields = ['pk']


