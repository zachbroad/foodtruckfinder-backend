from allauth.account.views import PasswordResetView
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, include, re_path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework import routers

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from trucks.models import Truck, Review

from announcements.api.views import AnnouncementViewSet
from catering.api.views import CateringViewSet
from django.views.generic.base import TemplateView
from events.api.views import EventViewSet
from notifications.api.views import NotificationViewSet
from onthegrub.views import IndexView
from users.api.views import AccountViewSet, FavoritesViewSet, FeedbackViewSet, ProfileViewSet
from users.api.views import CustomAuthToken, ValidateToken
from users.views import SignupView, SuccessView, LoginView, LogoutView
from trucks.api.views import TruckViewSet, ReviewsViewSet, VisitViewSet, DashboardViewSet, HomePage, MenuItemViewSet, \
    TagsViewSet, LiveViewSet, TruckLiveViewSet, TruckScheduleViewSet

router = routers.DefaultRouter()
router.register(r'announcements', AnnouncementViewSet)
router.register(r'caters', CateringViewSet)
router.register(r'dashboard', DashboardViewSet)
router.register(r'devices', FCMDeviceAuthorizedViewSet)
router.register(r'events', EventViewSet)
router.register(r'favorites', FavoritesViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'lives', LiveViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'notifications', NotificationViewSet, basename='Notifications')
router.register(r'profile', ProfileViewSet)
router.register(r'reviews', ReviewsViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'trucks', TruckViewSet)
router.register(r'schedules', TruckScheduleViewSet)
router.register(r'users', AccountViewSet)
router.register(r'visits', VisitViewSet)

truck_info_dict = {
    'queryset': Truck.objects.all(),
    'date_field': 'last_updated'
}

review_info_dict = {
    'queryset': Review.objects.all(),
    'date_field': 'post_edited',
}

api_patterns = [
    *router.urls,
    # "Home" Page
    path('home/', HomePage.as_view(), name='home'),
    path('trucks/<truck>/live', TruckLiveViewSet.as_view(), name='trucks-live')
]

urlpatterns = [
                  # Test site
                  path('', IndexView.as_view(), name='index'),

                  # robots.txt
                  path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), ),

                  # Account
                  path('accounts/', include('allauth.urls')),

                  path('users/', include('users.urls')),

                  path('signup/', SignupView.as_view(), name='grub-signup'),
                  path('login/', LoginView.as_view(), name='grub-login'),
                  path('logout/', LogoutView.as_view(), name='grub-logout'),
                  path('success/', SuccessView.as_view(), name='grub-success'),

                  path('users/', include('django.contrib.auth.urls')),

                  path('trucks/', include('trucks.urls')),
                  path('events/', include('events.urls')),
                  path('catering/', include('catering.urls')),
                  path('news/', include('announcements.urls')),

                  # Admin
                  path('admin/', admin.site.urls),

                  # Api
                  path('api/', include((api_patterns, '<int:pk>'), namespace='api')),

                  # Auth
                  path('api-auth/', include('rest_framework.urls')),
                  path('rest-auth/', include('rest_auth.urls')),
                  path('rest-auth/registration/', include('rest_auth.registration.urls')),
                  path('rest-auth/password/reset/', PasswordResetView.as_view(), name='password-reset'),
                  path('login-token/', CustomAuthToken.as_view(), name='login-token'),
                  path('validate-token/', ValidateToken.as_view(), name='validate-token'),
                  # markdown
                  url(r'^markdownx/', include('markdownx.urls')),
                  re_path('^static/(?P<path>.*)$', serve,
                          {'document_root': settings.STATIC_ROOT}),

                  ### SITEMAP
                    path("sitemap.xml", sitemap, {
                        'sitemaps': {
                            'trucks': GenericSitemap(info_dict=truck_info_dict, priority=1.0),
                            'reviews': GenericSitemap(info_dict=review_info_dict, priority=0.9)
                        }
                    }, name="django.contrib.sitemaps.views.sitemap")

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
