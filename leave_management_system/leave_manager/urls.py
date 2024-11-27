from django.urls import path
from . import views

app_name = 'leave_manager'

urlpatterns = [
    path('requests/', views.manager_leave_requests, name='manager_leave_requests'),
    path('approve/<int:leave_id>/', views.approve_or_reject_leave, name='approve_or_reject_leave'),
]
