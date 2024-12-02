from django.urls import path
from . import views

app_name = 'volunteers'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('opportunities/', views.browse_opportunities, name='opportunity_list'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Add this line
    path('register/', views.register_as_volunteer, name='register_as_volunteer'),
    path('apply/<int:opportunity_id>/', views.apply_for_opportunity, name='apply_for_opportunity'),
]
