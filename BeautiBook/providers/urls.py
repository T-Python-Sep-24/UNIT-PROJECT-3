from django.urls import path 
from . import views

app_name = "providers"

urlpatterns = [
    path('add/artist',views.add_artist_view,name="add_artist_view"),
    path('artists/',views.artists_view,name="artists_view"),
]