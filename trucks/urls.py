from django.urls import path

from . import views

app_name = 'trucks'

urlpatterns = [
    path('', views.TruckList.as_view(), name='index'),
    path('<pk>/menu/', views.menu, name='menu'),
    path('<pk>/menu/<item_id>/', views.MenuItemDetail.as_view(), name='menu-item'),
    path('<pk>/favorite/', views.FavoriteThisTruck.as_view(), name='favorite'),
    path('<pk>/unfavorite/', views.UnfavoriteThisTruck.as_view(), name='unfavorite'),
    path('<pk>/book/', views.BookCatering.as_view(), name='book-catering'),
    path('<pk>/book/success/', views.BookCateringSuccess.as_view(), name='book-catering-success'),
    path('<pk>/schedule/<event_id>/', views.TruckEventDetail.as_view(), name='event-detail'),
    path('<pk>/schedule/', views.TruckSchedule.as_view(), name='schedule'),
    path('<pk>/reviews/', views.ReviewList.as_view(), name='reviews'),
    path('<pk>/reviews/new/', views.ReviewCreate.as_view(), name='new-review'),
    path('<pk>/reviews/<review_id>/', views.ReviewDetail.as_view(), name='review-detail'),
    path('<pk>/', views.detail, name='detail'),
    # path('<truck_id>/reviews/<review_id>', views.ReviewDetailEditDelete),
]
