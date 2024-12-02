from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('add/', views.add_pet, name='add_pet'),
    path('list/', views.pet_list_view, name='pet_list_view'), 
    path('pet/<pet_id>/', views.pet_detail_view, name='pet_detail'),
    path('pet/<pet_id>/edit/', views.edit_pet, name='edit_pet'),
    path('pet/<pet_id>/delete/', views.delete_pet, name='delete_pet'), 
]