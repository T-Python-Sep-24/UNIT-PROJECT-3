from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest,HttpResponse
from .models import Photo,Artist
# Create your views here.

def artists_view(request:HttpRequest):
    artists = Artist.objects.all()
    return render(request,"providers/artists.html",{"artists":artists})

def add_artist_view(request:HttpRequest):
    artists = Artist.objects.all()  

    if request.method == "POST":
        new_artist = Artist(
        name=request.POST["name"],
        title=request.POST["title"],
        about = request.POST["about"],
        email = request.POST["email"],
        logo = request.FILES["logo"],
        insta_url=request.POST["insta_url"],  
        )
        new_artist.save()
        for img in request.FILES.getlist("image"):
            Photo.objects.create(artist=new_artist,image=img)
        return redirect("providers:add_artist_view")
    return render(request,"providers/add_artist.html")

def artist_detail_view(request:HttpRequest, artist_id:int):
    artist = Artist.objects.get(pk=artist_id)
    photos = Photo.objects.filter(artist=artist)
    return render(request,"providers/artist_detail.html",{"artist":artist,"photos":photos})

def update_artist_view(request: HttpRequest,artist_id:int):
    artist_detail = get_object_or_404(Artist,pk=artist_id)
    if request.method == "POST":
        artist_detail.name = request.POST["name"]
        artist_detail.about = request.POST["about"]
        artist_detail.title = request.POST["title"]
        artist_detail.email = request.POST["email"]
        artist_detail.logo = request.FILES["logo"]
        artist_detail.insta_url = request.POST["insta_url"]
        artist_detail.save()
        return redirect("dashboard:dashboard_view")
    return render(request, "providers/update_artist.html",{"artist_detail": artist_detail})

def artist_delete_view(request:HttpRequest, artist_id:int):
    artist_detail = Artist.objects.get(pk=artist_id)
    artist_detail.delete()
    return redirect("dashboard:dashboard_view")





