from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest,HttpResponse
from .models import Photo,Artist,Review
from django.contrib import messages
from django.core.paginator import Paginator


# Create your views here.

def artists_view(request:HttpRequest):
    artists = Artist.objects.all()
    paginator = Paginator(artists, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"providers/artists.html",{"artists":page_obj})

def add_artist_view(request:HttpRequest):
    artists = Artist.objects.all()  

    if request.method == "POST":
        new_artist = Artist(
        name=request.POST["name"],
        title=request.POST["title"],
        about = request.POST["about"],
        email = request.POST["email"],
        price_range = request.POST["price_range"],
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
        artist_detail.price_range = request.POST["price_range"]
        artist_detail.logo = request.FILES["logo"]
        artist_detail.insta_url = request.POST["insta_url"]
        artist_detail.save()
        return redirect("dashboard:dashboard_view")
    return render(request, "providers/update_artist.html",{"artist_detail": artist_detail})

def artist_delete_view(request:HttpRequest, artist_id:int):
    artist_detail = Artist.objects.get(pk=artist_id)
    artist_detail.delete()
    return redirect("dashboard:dashboard_view")


def add_review_view(request:HttpRequest, artist_id):
    if not request.user.is_authenticated:
        messages.error(request, "Only registered user can add review","alert-danger")
        return redirect("accounts:sign_in")
    if request.method == "POST":
        artist_object = Artist.objects.get(pk=artist_id)
        new_review = Review(artist=artist_object,user=request.user,comment=request.POST["comment"],rating=request.POST["rating"])
        new_review.save()
        messages.success(request, "Added Review Successfully", "alert-success")
    return redirect("providers:artist_detail_view", artist_id=artist_id)

def delete_review_view(request:HttpRequest, review_id):
    try:
        review = Review.objects.get(pk=review_id)
        artist_id=review.artist.id
        if not ( request.user.is_staff and request.user.has_perm("artists.delete_review")) and review.user != request.user:
            messages.warning(request, "You can't delete this review","alert-warning")
        else:
            review.delete()
            messages.success(request, "deleted review", "alert-success")
    except Exception as e:
        messages.error(request, "couldn't delete review", "alert-danger")
    return redirect("providers:artist_detail_view", artist_id=artist_id)
