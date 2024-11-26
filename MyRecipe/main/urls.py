from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('update-recipe/<int:recipe_id>/', views.update_recipe, name='update_recipe'),
    path('delete-recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('search/', views.search, name='search'),
]