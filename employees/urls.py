# employee_management/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='register'),
]
