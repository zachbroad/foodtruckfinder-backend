from django.urls import path

from users.views import SignupView, LoginView, LogoutView, UserList, UserDetail, SuccessView

app_name = 'users'

urlpatterns = [
    path('', UserList.as_view(), name='list'),
    path('<str:username>/', UserDetail.as_view(), name='detail'),
]
