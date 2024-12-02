from django.urls import path
from . import views

app_name = 'employee_leave'

urlpatterns = [
    path('request/', views.request_leave, name='request_leave'),
    path('requests/', views.leave_requests, name='leave_requests'),
]
