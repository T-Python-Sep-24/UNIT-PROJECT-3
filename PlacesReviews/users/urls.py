from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .views import CustomLoginView
from . import views


app_name = "users"

urlpatterns = [
    path(
        "register/",
        CreateView.as_view(
            template_name="users/register.html",
            form_class=UserCreationForm,
            success_url="/users/login/"
        ),
        name="register",
    ),
    path(
        "login/",
        CustomLoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page="/users/login/"),
        name="logout",
    ),

    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    
    path('bookmarks/', views.user_bookmarks_view, name='user_bookmarks'),

]
