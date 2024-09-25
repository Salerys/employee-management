# employee_management/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='register'),
    path(
        'logout/',
        LogoutView.as_view(next_page='/login'),
        name='logout',
    ),
    path('home/', views.home, name='home'),
    path('profile/<int:id>', views.get_profile_data, name='profile'),
    path('edit-profile/<int:id>', views.update_profile, name='edit-profile'),
    path('list/', views.employees_list, name='list'),
    path('edit-employee/<int:emp_id>', views.update_employee, name='edit-employee'),
    path('confirm-delete/<int:emp_id>', views.delete_employee, name='confirm-delete'),
    path('job-settings', views.job_settings, name='job-settings'),
]
