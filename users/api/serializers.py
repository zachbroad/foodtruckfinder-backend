from rest_framework import serializers

from onthegrub.util import Base64ImageField
from trucks.api.serializers import FavoriteTruckSerializer
from users.models import User, SearchTerm, Feedback


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
    profile_picture = Base64ImageField(
        max_length=None, use_url=True, required=False, allow_empty_file=False, allow_null=True
    )

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
            'favorite_trucks',
            
            'profile_picture',
            'biography',
        )
        read_only_fields = ['pk']


