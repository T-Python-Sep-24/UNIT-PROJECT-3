from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit-profile'),
    path('edit_skills/', views.edit_skills, name='edit-skills'),
    path('register/volunteer/', views.register_volunteer, name='register-volunteer'),
    path('register/company/', views.register_company, name='register-company'),
    path('login/', views.user_login, name='login'),
     path('logout/', views.user_logout, name='logout'), 

]
