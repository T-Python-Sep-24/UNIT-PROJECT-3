from django.urls import path
from . import views



app_name='accounts'

urlpatterns = [
    path('signup/',views.signup_view,name="signup_view"),
    path('signin/',views.signin_view,name="signin_view"),
    path('logout/',views.log_out,name="logout"),
    path('<user_name>/',views.profile_view,name='profile_view'),
    path('update/profile/',views.update_profile_view,name="update_profile_view"),
    path('update/budget/',views.update_budget_view,name='update_budget_view')

]