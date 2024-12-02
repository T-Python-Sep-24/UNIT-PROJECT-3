from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
   path('add/', views.add_donation_request, name='add_donation_request'),  
   path('list/', views.donation_request_list, name='donation_request_list'),
   path('delete/<donation_id>/', views.delete_donation_request, name='delete_donation_request'), 
   path('edit/<request_id>/', views.edit_donation_request, name='edit_donation_request'),
   #path('donate/<donation_request_id>/', views.make_donation, name='make_donation'),
   path('donate/medical/<donation_request_id>/', views.make_medical_donation, name='make_medical_donation'),
    path('donate/supplies/<int:donation_request_id>/', views.make_supply_donation, name='make_supply_donation'),
]
