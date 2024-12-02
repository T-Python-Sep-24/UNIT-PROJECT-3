from django.urls import path
from . import views


app_name="project"



urlpatterns=[
    path("project/",views.project_view,name="project_view"),
    path("dashboard/",views.dashboard_view,name="dashboard_view"),
    path("create/project",views.create_project_view,name="create_project_view"),
    path("detail/<project_id>/",views.project_detail_view,name="project_detail_view"),
    path('upload-file/<project_id>', views.upload_file, name='upload_file'),
    path('project/<int:project_id>/update/', views.update_project_view, name='update_project_view'),
     path("delete/<project_id>/", views.project_delete_view, name="project_delete_view"),
    

]