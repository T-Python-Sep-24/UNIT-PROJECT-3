from django.urls import path
from . import views

app_name='main'
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/<str:role>/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
]