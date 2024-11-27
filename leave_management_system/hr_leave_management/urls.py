from django.urls import path
from . import views

app_name = 'hr_leave_management'

urlpatterns = [
    path('dashboard/', views.hr_dashboard, name='hr_dashboard'),
    #path('login/', views.login_page, name='login'),
    #path('add_user/', views.add_user, name='add_user'),
    #path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    #path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('leave-requests/', views.leave_requests, name='leave_requests'),
    path('approve_reject_leave/<int:request_id>/', views.approve_reject_leave, name='approve_reject_leave'),
]
