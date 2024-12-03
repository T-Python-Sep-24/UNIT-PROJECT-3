from django.urls import path
from . import views



app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/organization/', views.register_organization, name='register_organization'),

]
