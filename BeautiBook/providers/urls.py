from django.urls import path 
from . import views

app_name = "providers"

urlpatterns = [
    path('add/artist',views.add_artist_view,name="add_artist_view"),
    path('artists/',views.artists_view,name="artists_view"),
    path('detail/<int:artist_id>',views.artist_detail_view,name="artist_detail_view"),
    path('update/<int:artist_id>',views.update_artist_view,name="update_artist_view"),
    path('delete/<int:artist_id>',views.artist_delete_view,name="artist_delete_view"),
    path("reviews/add/<artist_id>/", views.add_review_view, name="add_review_view"),
    path("reviews/delete/<review_id>/", views.delete_review_view, name="delete_review_view"),
]