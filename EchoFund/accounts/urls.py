from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('signin/', views.sign_in, name='sign_in'),
    path('signup/', views.sign_up, name='sign_up'),
    path('logout/', views.log_out, name='log_out'),
    path('profile/update', views.update_profile_view, name='update_profile_view'),
    path('profile/<user_name>/', views.profile_view, name='profile_view'),
]

