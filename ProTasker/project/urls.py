from django.urls import path
from . import views


app_name="project"



urlpatterns=[
    path("project/",views.project_view,name="project_view"),
    path("dashboard/",views.dashboard_view,name="dashboard_view"),
    path("create/project",views.create_project_view,name="create_project_view")
]