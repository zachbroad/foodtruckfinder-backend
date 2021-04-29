from django.urls import path

from users.views import UserList, UserDetail, UserTrucks, ReportUser, \
    UserEditProfile, UserReviews, UserFavorites

app_name = 'users'

urlpatterns = [
    path('', UserList.as_view(), name='list'),
    path('<str:username>/', UserDetail.as_view(), name='detail'),
    path('<str:username>/edit/', UserEditProfile.as_view(), name='edit-profile'),
    path('<str:username>/trucks/', UserTrucks.as_view(), name='user-trucks'),
    path('<str:username>/favorites/', UserFavorites.as_view(), name='user-favorites'),
    path('<str:username>/reviews/', UserReviews.as_view(), name='user-reviews'),
    path('<str:username>/report/', ReportUser.as_view(), name='user-report')
]
