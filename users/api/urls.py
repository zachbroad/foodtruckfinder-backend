from django.urls import path

from .views import AccountAPIView, AccountRUDView
from rest_framework import routers
from users.api.views import AccountViewSet

router = routers.DefaultRouter()
router.register(r'users', AccountViewSet)


urlpatterns = [
    path('/', AccountAPIView.as_view(), name='truck-create'),
    path('<int:pk>/', AccountRUDView.as_view(), name='truck-rud'),
    path(r'users/(?P<username>.+)/$', AccountAPIView.as_view()),
    
]

