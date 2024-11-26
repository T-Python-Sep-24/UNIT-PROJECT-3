from django.urls import path
from .import views


app_name = "opportunities"

urlpatterns = [
    path("all/", views.all_opportunities_view, name="all_opportunities_view"),
]