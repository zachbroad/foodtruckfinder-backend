from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from announcements.api.serializers import AnnouncementSerializer
from announcements.models import Announcement


class AnnouncementViewSet(ModelViewSet):
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()
    permission_classes = [permissions.AllowAny, ]
