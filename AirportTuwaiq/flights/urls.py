from django.urls import path
from . import views

app_name = "flights"

urlpatterns = [   
    path("add/flight" , views.add_flight_view , name="add_flight_view"),
    path('all/flight', views.flight_list_view, name='flight_list_view'),
    path('details/<flight_id>/', views.flight_detail_view, name='flight_detail_view'),
    path('edit/<flight_id>/', views.edit_flight_view, name='edit_flight_view'),
    path('delete/<int:flight_id>/', views.delete_flight_view, name='delete_flight_view'),
]
