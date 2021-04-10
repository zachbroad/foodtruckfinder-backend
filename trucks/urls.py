from django.urls import path
from . import views
app_name = 'trucks'

urlpatterns = [
    path('', views.index, name='index'),
    path('<truck_id>/', views.detail, name='detail'),
    path('<truck_id>/menu', views.menu, name='menu'),
    path('<truck_id>/schedule', views.TruckSchedule.as_view(), name='schedule'),
    path('<truck_id>/schedule/<event_id>/', views.TruckEventDetail.as_view(), name='event-detail'),
    path('<truck_id>/reviews/', views.ReviewListCreate.as_view(), name='reviews'),
    path('<truck_id>/reviews/new/', views.ReviewCreate.as_view(), name='new-review'),
    path('<truck_id>/reviews/<review_id>/', views.ReviewDetail.as_view(), name='review-detail'),
    # path('<truck_id>/reviews/<review_id>', views.ReviewDetailEditDelete),
]
