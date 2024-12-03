from django.urls import path
from .import views


app_name = "organizations"

urlpatterns = [
    path("all/", views.all_organizations_view, name="all_organizations_view"),
    path("new-opportunity/", views.add_opportunity_view, name="add_opportunity_view"),
    
]