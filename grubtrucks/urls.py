from allauth.account.views import PasswordResetView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, include, re_path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework import routers

from catering.views import CateringViewSet
from grubtrucks.views import index
from trucks.api.views import TruckViewSet, ReviewsViewSet, VisitViewSet, DashboardViewSet, HomePage, MenuItemViewSet, \
    TagsViewSet, LiveViewSet, TruckLiveViewSet
from users.api.views import AccountViewSet, FavoritesViewSet, FeedbackViewSet, ProfileView
from users.api.views import CustomAuthToken, ValidateToken

router = routers.DefaultRouter()
router.register(r'dashboard', DashboardViewSet)
router.register(r'favorites', FavoritesViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'reviews', ReviewsViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'trucks', TruckViewSet)
router.register(r'users', AccountViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'lives', LiveViewSet)
router.register(r'devices', FCMDeviceAuthorizedViewSet)
router.register(r'caters', CateringViewSet)

api_patterns = [
    *router.urls,
    # "Home" Page
    path('home/', HomePage.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('trucks/<truck>/live', TruckLiveViewSet.as_view(), name='trucks-live')
]

urlpatterns = [
    # Test site
    path('', index, name='index'),
    path('trucks/', include('trucks.urls'), name='trucks-index'),

    # Account
    path('accounts/', include('allauth.urls', )),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),

    # Admin
    path('admin/', admin.site.urls),

    # Api
    path('api/', include((api_patterns, '<int:pk>'), namespace='api-trucks')),

    # Auth
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/password/reset/', PasswordResetView.as_view(), name='password-reset'),
    path('login-token/', CustomAuthToken.as_view(), name='login-token'),
    path('validate-token/', ValidateToken.as_view(), name='validate-token'),
    re_path('^static/(?P<path>.*)$', serve,
          {'document_root': settings.STATIC_ROOT}),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
