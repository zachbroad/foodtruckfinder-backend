from rest_framework import serializers

from rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False, max_length=50)
    last_name = serializers.CharField(required=False, max_length=50)
    phone = serializers.CharField(required=False, max_length=20)

    def get_cleaned_data(self):
            return {
            'username' : self.validated_data.get('username',''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone',''),
        }