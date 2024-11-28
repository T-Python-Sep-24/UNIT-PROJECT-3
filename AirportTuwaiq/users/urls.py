from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('employee-signup', views.employee_sign_up_view , name='employee_sign_up_view'),   
    path('customer-signup/', views.customer_sign_up_view, name='customer_sign_up_view'),
    path('signin/', views.sign_in_view, name='sign_in_view'),
    path('logout/', views.logout_view, name='logout_view'), 
]