from django.shortcuts import render, redirect
from .models import Movie, Genre, Director, Screening
from .forms import MovieForm
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.contrib import messages
# Create your views here.


def add_movie_view(request:HttpRequest):
    movie_form=MovieForm()
    directors=Director.objects.all()
    genres=Genre.objects.all()

    if request.method == "POST":
        try:
            movie_form=MovieForm(request.POST,request.FILES)
            if movie_form.is_valid():
                movie_form.save()
                messages.success(request, "Created Movie Successfuly", "alert-success")
                return redirect('main:home_view')
            else:
                messages.error(request,movie_form.errors,'alert-danger')

        except Exception as e:
            print(e)
    return render(request,'movies/add_movie.html',context={'genres': genres, 'directors': directors})


def all_movies_view(request:HttpRequest):
    movies=Movie.objects.all()
    directors=Director.objects.all()
    genres=Genre.objects.all()
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        movies = Movie.objects.filter(title__contains=request.GET["search"])
        
    if "director" in request.GET and request.GET["director"]:
        
        movies = movies.filter(director__id=request.GET["director"])

    if "genre" in request.GET and request.GET["genre"]:
        movies = movies.filter(genre__id=request.GET["genre"])
    
    page_number = request.GET.get("page", 1)
    paginator = Paginator(movies, 10)
    movie_page = paginator.get_page(page_number)
    return render(request,"movies/all_movies.html",context={"movies":movie_page,"genres":genres,"directors":directors})


def movie_detail_view(request: HttpRequest, movie_id: int):
    movie = Movie.objects.get(pk=movie_id)
    
    
    screenings = movie.screening_set.all().order_by('showtime')
    
    screenings_by_date = {}
    
    
    for screening in screenings:
        screening_date = screening.showtime.date()
        
        if screening_date not in screenings_by_date:
            screenings_by_date[screening_date] = []
        
        screenings_by_date[screening_date].append(screening)
    
    for screening in screenings:
        available_seat = any(available for seat, available in screening.get_seats().items() if available)
        screening.is_available = available_seat
    
    return render(request, 'movies/movie_detail.html', context={'movie': movie, 'screenings_by_date': screenings_by_date})

def movie_update_view(request:HttpRequest,movie_id:int):
    movie=Movie.objects.get(pk=movie_id)
    if not request.user.is_staff:
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect('movies:movie_detail_view',movie_id=movie.id)
    
   
    directors=Director.objects.all()
    genres=Genre.objects.all()
    
    if request.method == 'POST':
        movie_form=MovieForm(instance=movie,data=request.POST,files=request.FILES)
        if movie_form.is_valid():
            movie_form.save()
            messages.success(request,' movie updated successfully','alert-success')
            return redirect('movies:movie_detail_view',movie_id=movie.id)
        else:
            messages.error(request,movie_form.errors,'alert-danger')
    return render(request,'movies/update_movie.html',context={'movie':movie,'directors':directors,'genres':genres})

def delete_movie_view(request:HttpRequest,movie_id:int):
    movie=Movie.objects.get(pk=movie_id)
    if not request.user.is_staff:
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect('movies:movie_detail_view',movie_id=movie.id)
    try:
            movie.delete()
            messages.success(request, f"Deleted {movie.title} successfully", "alert-success")
            return redirect ("movies:all_movies_view")
    except Exception as e:
            print(e)
            messages.error(request, f"Couldn't Delete {movie.title} ", "alert-danger")
            return redirect ("movies:all_movies_view")

