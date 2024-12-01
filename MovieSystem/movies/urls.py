from django.urls import path
from . import views



app_name='movies'

urlpatterns = [
    path('add/',views.add_movie_view,name="add_movie_view"),
    path('all/',views.all_movies_view,name="all_movies_view"),

]