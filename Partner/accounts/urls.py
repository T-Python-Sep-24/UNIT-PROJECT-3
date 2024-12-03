from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.sign_up, name="sign_up"),
    path('signin/', views.sign_in, name="sign_in"),
    path('logout/', views.log_out, name="log_out"),
    path('profile/update/', views.update_profile_view, name="update_profile_view"),
    path('profile/<user_name>/', views.user_profile_view, name="user_profile_view"),
    path('all/profiles/', views.all_partners_profiles_view, name="all_partners_profiles_view"),
]