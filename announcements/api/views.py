from rest_framework import permissions, pagination
from rest_framework.viewsets import ModelViewSet

from announcements.api.serializers import AnnouncementSerializer
from announcements.models import Announcement


class AnnouncementViewSet(ModelViewSet):
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()
    permission_classes = [permissions.AllowAny, ]
    pagination_class = pagination.LimitOffsetPagination
    page_size = 100
    # pagi

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update':
            self.permission_classes = [permissions.IsAdminUser, ]
        else:
            self.permission_classes = AnnouncementViewSet.permission_classes

        return super().get_permissions()
