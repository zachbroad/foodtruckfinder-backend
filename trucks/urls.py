from django.urls import path
from . import views
app_name = 'trucks'

urlpatterns = [
    path('', views.index, name='index'),
    path('<truck_id>/', views.detail, name='detail'),

]
