from rest_framework import serializers
from users.models import Account 


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'pk',
            'username',
            'email',
            'phone',
            'first_name',
            'last_name',

        )
        read_only_fields = ['pk']

