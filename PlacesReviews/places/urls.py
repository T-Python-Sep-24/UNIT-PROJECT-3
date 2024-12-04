from django.contrib import admin
from django.urls import path
from . import views

app_name="places"


urlpatterns = [
    path('', views.all_places_view, name='all_places_view'),               # List all places
    path('<int:pk>/', views.place_detail_view, name='place_detail_view'),  # View place details
    path('add/', views.add_place_view, name='add_place_view'),             # Add a new place
    path('search/', views.search_view, name='search_view'),                # Search places
    path('<int:pk>/delete/', views.delete_place_view, name='delete_place_view'),
    path('bookmarks/add/<int:place_id>/', views.add_bookmark_view, name='add_bookmark_view'),


]