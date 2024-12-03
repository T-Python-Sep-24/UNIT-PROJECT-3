from . import views
from django.urls import path

app_name="main"

urlpatterns=[
    path('',views.home_view,name="home_view"),
    path('language/add/',views.add_language_view,name="add_language_view"),
    path('language/edit/<lang_id>/',views.update_language_view,name="update_language_view"),
    path('language/delete/<lang_id>/',views.delete_language_view,name="delete_language_view"),
    path('language/search/', views.search_language, name='search_language'),

]