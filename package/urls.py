from django.urls import path
from . import views

urlpatterns = [
    path('', views.package, name='package'),
    path('<int:pk>/', views.package_details, name='package_details'),
]
