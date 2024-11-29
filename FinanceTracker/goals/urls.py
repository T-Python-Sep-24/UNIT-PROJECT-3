from django.urls import path
from . import views

app_name = 'goals' 

urlpatterns = [
    path('add_goal/', views.add_goal, name='add_goal'),
    path('goal/<int:goal_id>/', views.goal_detail, name='goal_detail'),

]
