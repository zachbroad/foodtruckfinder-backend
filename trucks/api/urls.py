from .views import MenuItemViewSet, ReviewsViewSet, VisitViewSet, TagsViewSet, LiveViewSet, TruckViewSet, TruckLiveViewSet
from rest_framework import routers
from django.urls import path


router = routers.DefaultRouter()
router.register(r'trucks', TruckViewSet)
router.register(r'reviews', ReviewsViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'menu items', MenuItemViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'lives', LiveViewSet)
router.register(r'live', TruckLiveViewSet)

urlpatterns = [
]

