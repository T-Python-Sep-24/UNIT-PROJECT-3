from django.urls import path
from . import views

app_name='directors'

urlpatterns = [
    path('all/',views.all_directors_view,name='all_directors_view'),
    path('detail/<director_id>/', views.director_detail_view, name='director_detail_view'),
    path('add/', views.add_director_view, name='add_director_view'),
    path('update/<director_id>/', views.director_update_view, name='director_update_view'),
    path('delete/<director_id>/', views.delete_director_view, name='delete_director_view'),
    
]