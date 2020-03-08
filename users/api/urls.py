from django.urls import path
from rest_framework import routers
from users.api.views import AccountViewSet, FavoritesViewSet

router = routers.DefaultRouter()
router.register(r'users', AccountViewSet)
router.register(r'favorites', FavoritesViewSet)

urlpatterns = [


]

