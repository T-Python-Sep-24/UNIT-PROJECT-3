from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('' , views.home_view, name='home_view' ),
    path('city/riyadh/', views.riyadh_view, name='riyadh'),
    path('jeddah/', views.jeddah_view, name='jeddah'),
    path('abha/', views.abha_view, name='abha'),
    path('dammam/', views.dammam_view, name='dammam'),
]