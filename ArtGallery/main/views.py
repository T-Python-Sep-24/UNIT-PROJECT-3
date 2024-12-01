from django.shortcuts import render
from django.http import HttpRequest

from artists.models import Artist
from artPieces.models import ArtPiece

# Home View
def homeView(request: HttpRequest):
    pieces = ArtPiece.objects.all().order_by('-addedAt')[:4]
    artists = Artist.objects.all().order_by('-addedAt')[:4]
    
    return render(request, 'main/index.html', {'pieces': pieces, 'artists': artists})
