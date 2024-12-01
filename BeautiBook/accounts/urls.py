from django.urls import path 
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/',views.signup_view,name="signup_view"),  
    path('signin/',views.signin_view,name="signin_view"),  
    path("logout",views.logout_view,name="logout_view"),
    path("profile/<user_name>",views.user_profile_view,name="user_profile_view"),
]