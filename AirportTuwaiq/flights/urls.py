from django.urls import path
from . import views

app_name = "flights"

urlpatterns = [   
    path("add/flight" , views.add_flight_view , name="add_flight_view")
]