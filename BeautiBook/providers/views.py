from django.shortcuts import render,redirect
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
        insta_url=request.POST["insta_url"],  
        )
        new_artist.save()
        for img in request.FILES.getlist("image"):
            Photo.objects.create(artist=new_artist,image=img)
        return redirect("providers:add_artist_view")
    return render(request,"providers/add_artist.html")



