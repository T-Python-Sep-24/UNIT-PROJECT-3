from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('search/', views.search_view, name='search_view'),
    path('contact/', views.contact_view, name='contact_view'),
    path('rate/add', views.rate_us_view, name='rate_us_view'),

]