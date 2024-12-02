from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path('', views.task_list, name="task_list"),
    path('create/', views.create_task, name="create_task"),
    path('<int:pk>/', views.task_detail, name='task_detail'),  
    path('<int:pk>/update/', views.update_task, name='update_task'),
    path('<int:task_id>/delete/', views.delete_task, name="delete_task"),
    path("add/<int:task_id>/", views.add_comment, name="add_comment"),
]
