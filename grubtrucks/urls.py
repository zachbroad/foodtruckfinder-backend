"""grubtrucks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from grubtrucks import settings
from rest_framework import routers
from django.conf.urls.static import static

from .views import index
from trucks.views import TruckViewSet, MenuItemViewSet

router = routers.DefaultRouter()
router.register(r'trucks', TruckViewSet)
router.register(r'menu-items', MenuItemViewSet)

urlpatterns = [
    path(r'', index, name='index'),
    path(r'trucks/', include('trucks.urls'), name='trucks-index'),
    path(r'admin/', admin.site.urls),
    path(r'api/', include((router.urls, '<int:pk>'), namespace='api-trucks')),
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'rest-auth/', include('rest_auth.urls')),
    path(r'rest-auth/registration/', include('rest_auth.registration.urls')),
    path(r'accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
