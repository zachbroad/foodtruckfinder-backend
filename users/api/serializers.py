from rest_framework import serializers
from users.models import Account 


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['pk',
                  'first_name',
                  'last_name',
                  'email',
                  'username',
                  'password',
                  ]
        read_only_fields = ['pk']

