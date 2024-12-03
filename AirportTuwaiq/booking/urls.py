from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
   path('search/', views.search_flights_view, name='search_flights'),
    path('booking/details/<int:flight_id>/', views.booking_detail_view, name='booking_detail'),
    path('filter/', views.filter_flights_view, name='filter_flights'),
    path('booking/confirm/<int:flight_id>/', views.confirm_booking_view, name='confirm_booking'),  # Confirm Booking
]