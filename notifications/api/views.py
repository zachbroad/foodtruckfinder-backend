from rest_framework import viewsets, permissions, exceptions
from ..models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            notifications = Notification.objects.get(user=user)
        except Notification.DoesNotExist:
            raise exceptions.NotFound('No notifications found')
        return 

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update':
            self.permission_classes = [permissions.IsAdminUser, ]
        else:
            self.permission_classes = NotificationViewSet.permission_classes

        return super().get_permissions()
