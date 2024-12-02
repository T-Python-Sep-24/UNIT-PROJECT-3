from django.urls import path
from . import views



app_name='movies'

urlpatterns = [
    path('add/',views.add_movie_view,name="add_movie_view"),
    path('all/',views.all_movies_view,name="all_movies_view"),
    path('detail/<movie_id>/',views.movie_detail_view,name="movie_detail_view"),
    path('update/<movie_id>/',views.movie_update_view,name="movie_update_view"),
    path('delete/<movie_id>/',views.delete_movie_view,name="delete_movie_view"),
    
    path('genres/all/',views.all_genres_view,name='all_genres_view'),
    path('genres/add/',views.add_genre_view,name='add_genre_view'),
    path('genre/update/<genre_id>/',views.update_genre_view,name='update_genre_view'),
    path('genres/remove/<genre_id>/',views.delete_genre_view,name='delete_genre_view'),

]