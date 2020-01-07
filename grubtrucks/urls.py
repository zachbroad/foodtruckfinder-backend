from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from allauth.account.views import PasswordResetView
from rest_framework import routers
from grubtrucks.views import index
from trucks.api.views import TruckViewSet
from users.views import AccountViewSet
from users.api.views import CustomAuthToken, ValidateToken

router = routers.DefaultRouter()
router.register(r'trucks', TruckViewSet)
router.register(r'users', AccountViewSet)

urlpatterns = [

        # Test site
        path(r'', index, name='index'),
        path(r'trucks/', include('trucks.urls'), name='trucks-index'),

        # Account
        path(r'accounts/', include('allauth.urls', )),
        path('users/', include('users.urls')),
        path('users/', include('django.contrib.auth.urls')),

        # Admin
        path(r'admin/', admin.site.urls),

        # Api
        path(r'api/', include((router.urls, '<int:pk>'), namespace='api-trucks')),

        # Auth
        path(r'api-auth/', include('rest_framework.urls')),
        path(r'rest-auth/', include('rest_auth.urls')),
        path(r'rest-auth/registration/', include('rest_auth.registration.urls')),
        path(r'rest-auth/password/reset/', PasswordResetView.as_view(), name='password-reset'),
        path('login-token/', CustomAuthToken.as_view(), name='login-token'),
        path('validate-token/', ValidateToken.as_view(), name='validate-token'),
        re_path(r'^static/(?P<path>.*)$', serve,
                {'document_root': settings.STATIC_ROOT}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
