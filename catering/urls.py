from django.urls import path

from . import views

app_name = 'catering'

urlpatterns = [
    path('', views.CaterList.as_view(), name='index'),
    path('<pk>/', views.CaterDetail.as_view(), name='detail'),
]
