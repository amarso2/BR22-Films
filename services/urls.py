
from django.urls import path
from . import views


urlpatterns = [
    path('', views.services, name='services'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
]
