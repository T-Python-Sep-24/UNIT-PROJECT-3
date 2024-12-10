from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from artPieces.models import ArtPiece
from .models import Artist
from .forms import ArtistForm
from django.core.paginator import Paginator

# Add artist View
def addArtistView(request: HttpRequest):

    if not (request.user.is_staff and request.user.has_perm('artists.add_artist')):
        messages.warning(request, "Only editors can add artists.", "alert-warning")
        response = redirect('main:homeView')
    else:
        artistData = ArtistForm()
        response = render(request, 'artists/addArtist.html')
        
        if request.method == "POST":
            artistData = ArtistForm(request.POST, request.FILES)
            if artistData.is_valid():
                artistData.save()
                messages.success(request, f"Artist '{request.POST['fullName']}' was added successfully.", "alert-success")
            else:
                messages.error(request, f"Artist '{request.POST['fullName']}' wasn't added.", "alert-danger")
                
            response = redirect('artists:displayArtistsView')
    
    return response

# Update artist View
def updateArtistView(request: HttpRequest, artistId:int):

    if not (request.user.is_staff and request.user.has_perm('artists.change_artist')):
        messages.warning(request, "Only editors can update artists.", "alert-warning")
        return redirect('main:homeView')
    else:
        try:
            artist = Artist.objects.get(pk=artistId)
        except Exception:
            return render(request, '404.html')
        else:
            response = render(request, 'artists/updateArtist.html', {'artist': artist})    
            if request.method == "POST":
                artistData = ArtistForm(request.POST, request.FILES, instance=artist)
                if artistData.is_valid():
                    artistData.save()
                    messages.success(request, f"Artist '{request.POST['fullName']}' was updated successfully.", "alert-success")
                else:
                    messages.error(request, f"Artist '{request.POST['fullName']}' wasn't updated.", "alert-danger")
                   
                response =  redirect('artists:displayArtistsView')
    
    return response

# Delete artist View
def deleteArtistView(request: HttpRequest, artistId:int):

    if not (request.user.is_staff and request.user.has_perm('artists.delete_artist')):
        messages.warning(request, "Only editors can delete artists.", "alert-warning")
        return redirect('main:homeView')
    else:
        try:
            artist = Artist.objects.get(pk=artistId)
        except Exception:
            response = render(request, '404.html')
        else:
            try:
                artist.delete()
            except Exception:
                messages.error(request, f"'{artist.fullName}' wasn't deleted.", "alert-danger")
            else: 
                messages.success(request, f"'{artist.fullName}' deleted successfully.", "alert-success") 
                response = redirect('artists:displayArtistsView')

    return response

# Artist details View
def artistDetailsView(request: HttpRequest, artistId:int):
    try:
        artist = Artist.objects.get(pk=artistId)
    except Exception:
        response = render(request, '404.html')
    else:

        relatedPieces = ArtPiece.objects.filter(artist=artist)[0:3]

        response = render(request, 'artists/artistDetails.html', {'artist': artist, 'relatedPieces': relatedPieces})
    return response

# Display artists View
def displayArtistsView(request: HttpRequest):

    artists = Artist.objects.all().order_by('-addedAt')
    
    if 'search' in request.GET and len(request.GET['search']) >= 2:
        artists = artists.filter(fullName__contains=request.GET['search'])

    paginator = Paginator(artists, 6)
    pageNumber = request.GET.get('page', 1)
    page_obj = paginator.get_page(pageNumber)

    response = render(request, 'artists/displayArtists.html', {'artists': page_obj})
    
    return response
