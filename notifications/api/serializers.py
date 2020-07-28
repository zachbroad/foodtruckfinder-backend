from ..models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()

    class Meta:
        model = Notification
        fields = [
            'pk',
            'title',
            'description',
            'posted_on',
            'user',
            'route',
            'webview_route',
        ]
