from django.urls import path

from .views import DashboardIndex, DashboardCateringIndex, DashboardEditTruck, DashboardMyTrucksList, \
    DashboardTruckDetail, DashboardNotifications, DashboardCateringDetail, DashboardCaterRequestResponse, DashboardViewTruckMenu, \
    DashboardEditTruckMenu, DashboardViewTruckMenuItem, DashboardCreateItem, DashboardDeleteMenuItem, DashboardEditMenuItem

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
    path('trucks/<pk>/menu/', DashboardViewTruckMenu.as_view(), name='view-menu'),
    path('trucks/<pk>/menu/add/', DashboardCreateItem.as_view(), name='add-item'),
    path('trucks/<pk>/menu/<item_id>/delete/', DashboardDeleteMenuItem.as_view(), name='delete-menu-item'),
    path('trucks/<pk>/menu/<item_id>/edit/', DashboardEditMenuItem.as_view(), name='edit-menu-item'),
    path('trucks/<pk>/menu/<item_id>/', DashboardViewTruckMenuItem.as_view(), name='view-menu-item'),
    # path('trucks/<pk>/menu/edit/', DashboardEditTruckMenu.as_view(), name='edit-menu'),

    # Notifications
    path('notifications/', DashboardNotifications.as_view(), name='notifications'),
]
