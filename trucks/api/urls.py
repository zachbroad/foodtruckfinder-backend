
from .views import MenuItemViewSet, MenuItemDetailView, ReviewsViewSet, VisitViewSet
from django.urls import path
from rest_framework import routers

from trucks.api.views import TruckViewSet

router = routers.DefaultRouter()
router.register(r'trucks', TruckViewSet)
router.register(r'reviews', ReviewsViewSet)
router.regiser(r'visits', VisitViewSet)
router.register(r'menu items', MenuItemViewSet)

urlpatterns = [
    # path('/', TruckListView.as_view(), name='truck-create'),
    # path('<int:pk>/', TruckDetailView.as_view(), name='truck-rud'),
    # path('<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-rud')
]

