from django.urls import path

from users.views import SignupView, LoginView, LogoutView, UserList, UserDetail, SuccessView

app_name = 'users'

auth_urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('success/', SuccessView.as_view(), name='success'),
]

user_urlpatterns = [
    path('', UserList.as_view(), name='list'),
    path('<str:username>/', UserDetail.as_view(), name='detail'),
]

urlpatterns = [
]
