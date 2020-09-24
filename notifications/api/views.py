from rest_framework import exceptions, permissions, status, viewsets
from ..models import Notification
from .serializers import NotificationSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            notifications = Notification.objects.filter(user=user.pk)
            return notifications
        except Notification.DoesNotExist:
            raise exceptions.NotFound('No notifications found')

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update':
            self.permission_classes = [permissions.IsAdminUser, ]
        else:
            self.permission_classes = NotificationViewSet.permission_classes

        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        data = request.data

        try:
            notification = self.get_object()
            seen = data.get('seen', None)

            if seen is not None:
                print(seen)
                notification.seen = (seen == 'true')
        except Notification.DoesNotExist:
            raise ValidationError('Notification doesn\'t exist')
        except Exception as e:
            return Response("Error: {}".format(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        notification.save()
        serializer = NotificationSerializer(
            notification, many=False, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
