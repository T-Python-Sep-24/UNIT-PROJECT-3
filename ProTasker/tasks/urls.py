from django.urls import path
from . import views



app_name="tasks"

urlpatterns=[

path("task/",views.task_view,name="task_view"),
path("create_task/",views.create_task,name="create_task"),
path("update/task/<task_id>/",views.update_task,name="update_task"),
 path("delete/<task_id>/", views.task_delete_view, name="task_delete_view"),

]