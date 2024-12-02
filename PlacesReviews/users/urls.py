from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from . import views


app_name = "users"

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    path('bookmarks/', views.user_bookmarks_view, name='user_bookmarks'),
    path('signin/', views.sign_in, name='signin'),
    path('logout/', views.log_out, name='logout'),

]
