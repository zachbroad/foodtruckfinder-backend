from django.urls import path

from users.views import SignupView, LoginView, LogoutView, UserList, UserDetail

app_name = 'users'
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<str:username>/', UserDetail.as_view(), name='detail'),
    path('', UserList.as_view(), name='list'),
]
