from django.urls import path

from . import views

app_name = 'announcements'

urlpatterns = [
    path('', views.AnnouncementList.as_view(), name='index'),
    path('<pk>/', views.AnnouncementDetail.as_view(), name='detail'),
]
