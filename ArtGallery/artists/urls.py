from django.urls import path
from . import views

app_name = "artists"

urlpatterns = [
    path('add/', views.addArtistView, name="addArtistView"),
    path('update/<int:artistId>', views.updateArtistView, name="updateArtistView"),
    path('delete/<int:artistId>', views.deleteArtistView, name="deleteArtistView"),
    path('artistDetails/<int:artistId>', views.artistDetailsView, name="artistDetailsView"),
    path('all/', views.displayArtistsView, name="displayArtistsView"),
]