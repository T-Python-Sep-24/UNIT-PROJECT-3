from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    path('list/', views.organization_list, name='organization_list'),
    path('opportunities/', views.opportunity_list, name='opportunity_list'),
    path('opportunity/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('add_opportunity/', views.add_opportunity, name='add_opportunity'),
]
