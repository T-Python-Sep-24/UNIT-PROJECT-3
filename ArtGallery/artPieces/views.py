from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from artPieces.models import ArtPiece, Attachment
from artPieces.forms import ArtPieceForm
from artists.models import Artist
from django.core.paginator import Paginator
from django.db.models import Count
from accounts.models import Favorite


# Add art piece View
def addArtPieceView(request: HttpRequest):

    if not (request.user.is_staff and request.user.has_perm('artpieces.add_artpiece')):
        messages.warning(request, "Only editors can add art pieces.", "alert-warning")
        response = redirect('main:homeView')
    else:
        pieceData = ArtPieceForm()
        artists = Artist.objects.all()
        response = render(request, 'artPieces/addPiece.html', context={'artists': artists})
        
        if request.method == "POST":
            pieceData = ArtPieceForm(request.POST)
            images = request.FILES.getlist('images')
            if pieceData.is_valid():
                piece:ArtPiece = pieceData.save(commit=False)
                piece.save()
                for img in images:
                    Attachment.objects.create(piece=piece, image=img)
                messages.success(request, f"'{request.POST['name']}' was added successfully.", "alert-success")
            else:
                messages.error(request, f"'{request.POST['name']}' wasn't added.", "alert-danger")
                
            # response = redirect('artPieces:displayPiecesView', 'all')
            response = redirect('main:homeView')
    
    return response

# Update art piece View
def updateArtPieceView(request: HttpRequest, pieceId:int):

    if not (request.user.is_staff and request.user.has_perm('artpieces.change_artpiece')):
        messages.warning(request, "Only editors can update art pieces.", "alert-warning")
        response = redirect('main:homeView')
    else:
        try:
            piece = ArtPiece.objects.get(pk=pieceId)
        except Exception:
            response = render(request, '404.html')
        else:
            pieceData = ArtPieceForm()
            artists = Artist.objects.all()
            response = render(request, 'artPieces/updatePiece.html', {'piece': piece, 'artist': artists})
            
            if request.method == "POST":
                pieceData = ArtPieceForm(request.POST, instance=piece)
                images = request.FILES.getlist('images')
                if pieceData.is_valid():
                    piece:ArtPiece = pieceData.save(commit=False)
                    piece.save()
                    piece.colors.set(request.POST.getlist("colors"))
                    if images:
                        Attachment.objects.filter(piece=piece).delete()
                        for img in images:
                            Attachment.objects.create(piece=piece, image=img)
                    
                    messages.success(request, f"'{request.POST['name']}' was updated successfully.", "alert-success")
                else:
                    messages.error(request, f"'{request.POST['name']}' wasn't updated.", "alert-danger")
                    
                # response = redirect('artPieces:pieceDetailsView', pieceId)
                response = redirect('main:homeView')

    return response

# Delete art piece View
def deleteArtPieceView(request: HttpRequest, pieceId:int):

    if not (request.user.is_staff and request.user.has_perm('artpieces.delete_artpiece')):
        messages.warning(request, "Only editors can delete art pieces.", "alert-warning")
        response = redirect('main:homeView')
    else:
        try:
            piece = ArtPiece.objects.get(pk=pieceId)
        except Exception:
            response = render(request, '404.html')
        else:
            try:
                piece.delete()
            except Exception:
                messages.error(request, f"'{piece.name}' wasn't deleted.", "alert-danger")
            else: 
                messages.success(request, f"'{piece.name}' deleted successfully.", "alert-success")    
            
            # response = redirect('artPieces:displayPiecesView', 'all')

    return response
