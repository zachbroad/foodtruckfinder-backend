from rest_framework import serializers
from users.models import Account, SearchTerm


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

        )
        read_only_fields = ['pk']
