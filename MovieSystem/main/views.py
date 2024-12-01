from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from movies.models import Movie
# Create your views here.


def home_view(request:HttpRequest):
    movies = Movie.objects.all().order_by("-release_date")[0:3]
    
    return render(request,"main/index.html",context={'movies':movies})