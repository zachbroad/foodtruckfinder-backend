from django.urls import path
from .views import DashboardIndex, DashboardCateringIndex, DashboardEditTruck, DashboardMyTrucksList, \
    DashboardTruckDetail, DashboardNotifications

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardIndex.as_view(), name='index'),
    path('catering/',  DashboardCateringIndex.as_view(), name='catering-index'),
    path('trucks/', DashboardMyTrucksList.as_view(), name='truck-list'),
    path('trucks/<int:truck_id>/', DashboardTruckDetail.as_view(), name='truck-detail'),
    path('trucks/<int:truck_id>/edit/', DashboardEditTruck.as_view(), name='edit'),
    path('notifications/', DashboardNotifications.as_view(), name='notifications'),
]
