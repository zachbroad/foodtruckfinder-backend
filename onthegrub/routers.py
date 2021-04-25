from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

from announcements.api.views import AnnouncementViewSet
from catering.api.views import CateringViewSet
from events.api.views import EventViewSet
from notifications.api.views import NotificationViewSet
from trucks.api.views import TruckViewSet, ReviewsViewSet, VisitViewSet, MenuItemViewSet, \
    TagsViewSet, LiveViewSet, TruckScheduleViewSet, FavoritesViewSet
from users.api.views import AccountViewSet, FeedbackViewSet, ProfileViewSet


class GrubRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'announcements', AnnouncementViewSet)
        self.register(r'caters', CateringViewSet)
        self.register(r'devices', FCMDeviceAuthorizedViewSet)
        self.register(r'events', EventViewSet)
        self.register(r'favorites', FavoritesViewSet)
        self.register(r'feedback', FeedbackViewSet)
        self.register(r'lives', LiveViewSet)
        self.register(r'menu-items', MenuItemViewSet)
        self.register(r'notifications', NotificationViewSet, basename='Notifications')
        self.register(r'profile', ProfileViewSet)
        self.register(r'reviews', ReviewsViewSet)
        self.register(r'tags', TagsViewSet)
        self.register(r'trucks', TruckViewSet)
        self.register(r'schedules', TruckScheduleViewSet)
        self.register(r'users', AccountViewSet)
        self.register(r'visits', VisitViewSet)
