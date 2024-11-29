from django.urls import path
from . import views

app_name = "artPieces"

urlpatterns = [
    path('add/', views.addArtPieceView, name="addArtPieceView"),
    path('update/<int:pieceId>', views.updateArtPieceView, name="updateArtPieceView"),
    path('delete/<int:pieceId>', views.deleteArtPieceView, name="deleteArtPieceView"),
]