from django.urls import path
from .import views


app_name = "accounts"

urlpatterns = [
    path("org/signup/", views.organization_signup_view, name="organization_signup_view"),
    path("vol/signup/", views.volunteer_signup_view, name="volunteer_signup_view"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("org/<str:username>/profile/", views.organization_profile, name='organization_profile'),
    path("vol/<str:username>/profile/", views.volunteer_profile, name='volunteer_profile'),
    path("org/<str:username>/update/", views.organization_update_profile, name='organization_update_profile'),
    path("vol/<str:username>/update/", views.volunteer_update_profile, name='volunteer_update_profile'),


]