from django.urls import path
from .import views


app_name = "accounts"

urlpatterns = [
    path("org/signup/", views.organization_signup_view, name="organization_signup_view"),
    path("vol/signup/", views.volunteer_signup_view, name="volunteer_signup_view"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
]