from allauth.account.views import PasswordResetView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, include, re_path
from rest_framework import routers

from grubtrucks.views import index
from trucks.api.views import TruckViewSet, ReviewsViewSet, VisitViewSet, DashboardViewSet, HomePage, MenuItemViewSet, \
    TagsViewSet
from users.api.views import AccountViewSet, FavoritesViewSet, FeedbackViewSet, ProfileView
from users.api.views import CustomAuthToken, ValidateToken

router = routers.DefaultRouter()
router.register(r'trucks', TruckViewSet)
router.register(r'users', AccountViewSet)
router.register(r'reviews', ReviewsViewSet)
router.register(r'favorites', FavoritesViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'dashboard', DashboardViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'tags', TagsViewSet)

api_patterns = [
    *router.urls,
    # "Home" Page
    path('home/', HomePage.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile')
]

urlpatterns = [

                  # Test site
                  path(r'', index, name='index'),
                  path('trucks/', include('trucks.urls'), name='trucks-index'),

                  # Account
                  path('accounts/', include('allauth.urls', )),
                  path('users/', include('users.urls')),
                  path('users/', include('django.contrib.auth.urls')),

                  # Admin
                  path(r'admin/', admin.site.urls),

                  # Api
                  path(r'api/', include((api_patterns, '<int:pk>'), namespace='api-trucks')),

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
