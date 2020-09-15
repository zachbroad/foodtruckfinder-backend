from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventList.as_view(), name='index'),
    path('<pk>/', views.EventDetail.as_view(), name='detail'),
]