from django.urls import path
from . import views


app_name="project"



urlpatterns=[
    path("project/",views.project_view,name="project_view")
]