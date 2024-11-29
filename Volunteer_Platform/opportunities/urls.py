from django.urls import path
from . import views

urlpatterns = [
    path('', views.OpportunityListView.as_view(), name='opportunity-list'),
    path('<int:pk>/', views.OpportunityDetailView.as_view(), name='opportunity-detail'),
    path('create/', views.OpportunityCreateView.as_view(), name='opportunity-create'),
]
