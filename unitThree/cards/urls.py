from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.home_views, name='home_views'),
    path('create-folder/', views.create_folder_views, name='create_folder_views'),
    path('folders/', views.folder_list, name='folder_list'),
    path('folder/<int:folder_id>/', views.folder_detail_view, name='folder_detail'),
    path('folder/<int:folder_id>/add-flashcard/', views.create_flashcard_view, name='create_flashcard_view'),
    path('folder/<int:folder_id>/delete/', views.folder_delete_view, name='folder_delete'),  

]
