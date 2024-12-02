from django.urls import path
from . import views

app_name = 'volunteers'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_as_volunteer, name='register_as_volunteer'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('browse/', views.browse_opportunities, name='opportunity_list'),  # Update or add this
    path('apply/<int:opportunity_id>/', views.apply_for_opportunity, name='apply_for_opportunity'),
]
