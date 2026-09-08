
from django.urls import path
from . import views


urlpatterns = [
    path('', views.services, name='services'),
    path('<int:pk>/', views.services_details, name='service_detail'),
]
