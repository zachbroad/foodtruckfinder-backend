from django.urls import path

from .views import DashboardIndex, DashboardCateringIndex, DashboardEditTruck, DashboardMyTrucksList, \
    DashboardTruckDetail, DashboardNotifications, DashboardCateringDetail, DashboardCaterRequestResponse

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardIndex.as_view(), name='index'),

    # Catering
    path('catering/', DashboardCateringIndex.as_view(), name='catering-index'),
    path('catering/<pk>/', DashboardCateringDetail.as_view(), name='catering-request-detail'),
    path('catering/<pk>/modify/', DashboardCaterRequestResponse.as_view(), name='catering-request-modify'),

    # Trucks
    path('trucks/', DashboardMyTrucksList.as_view(), name='truck-list'),
    path('trucks/<pk>/', DashboardTruckDetail.as_view(), name='truck-detail'),
    path('trucks/<pk>/edit/', DashboardEditTruck.as_view(), name='edit'),

    # Notifications
    path('notifications/', DashboardNotifications.as_view(), name='notifications'),
]
