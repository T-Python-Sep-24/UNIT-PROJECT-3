from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/individual/', views.register_individual_view, name='register_individual'),
    path('register/shelter/', views.register_shelter_view, name='register_shelter'),
    path('profile/individual/<individual_id>/', views.individual_profile, name='individual_profile'),
    path('profile/edit/<individual_id>', views.edit_individual_profile, name='individual_edit_profile'),
    path('profile/shelter/<shelter_id>/', views.shelter_profile, name='shelter_profile'),
    path('profile/shelter/edit/<shelter_id>/', views.edit_shelter_profile, name='shelter_edit_profile'),  
]



