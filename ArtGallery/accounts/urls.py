from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.registerView, name="registerView"),
    path('login/', views.loginView, name="loginView"),
    path('logout/', views.logoutView, name="logoutView"),
    path('profile/update/', views.updateProfileView, name="updateProfileView"),
    path('profile/<username>/', views.profileView, name="profileView"),
]