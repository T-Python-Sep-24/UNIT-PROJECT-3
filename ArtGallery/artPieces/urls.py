from django.urls import path
from . import views

app_name = "artPieces"

urlpatterns = [
    path('add/', views.addArtPieceView, name="addArtPieceView"),
    path('update/<int:pieceId>', views.updateArtPieceView, name="updateArtPieceView"),
    path('delete/<int:pieceId>', views.deleteArtPieceView, name="deleteArtPieceView"),
    path('artpieceDetails/<int:pieceId>', views.artPieceDetailsView, name="artPieceDetailsView"),
    path('<filter>/', views.displayArtPiecesView, name="displayArtPiecesView"),

    path('comment/add/<int:pieceId>', views.addCommentView, name="addCommentView"),
    path('comment/delete/<int:commentId>', views.deleteCommentView, name="deleteCommentView"),
]