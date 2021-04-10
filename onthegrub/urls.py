import debug_toolbar
from allauth.account.views import PasswordResetView
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView

from onthegrub.views import IndexView
from trucks.api.views import HomePage, TruckLiveViewSet
from users.api.views import CustomAuthToken, ValidateToken
from users.views import SignupView, SuccessView, LoginView, LogoutView

from .routers import GrubRouter
from .sitemap import sitemap

router = GrubRouter()

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
                  path('dashboard/', include('dashboard.urls')),

                  # Admin

                  path('admin/', admin.site.urls),
                  path('__debug__/', include(debug_toolbar.urls)),

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

                  *sitemap

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
