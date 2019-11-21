from django.urls import path

from .views import AccountAPIView, AccountRUDView
from rest_framework import routers
from users.views import AccountViewSet

router = routers.DefaultRouter()
router.register(r'trucks', AccountViewSet)


urlpatterns = [
    path('/', AccountAPIView.as_view(), name='truck-create'),
    path('<int:pk>/', AccountRUDView.as_view(), name='truck-rud'),
]

