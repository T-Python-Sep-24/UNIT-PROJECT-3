from django.urls import path
from . import views

app_name = 'groups' 

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('create/', views.create_group, name='create_group'),
    path('<int:group_id>/', views.group_detail, name='group_detail'),
    path('group/<int:group_id>/add_goal/', views.add_or_update_goal, name='add_goal'),
    path('group/<int:group_id>/add_expense/', views.add_or_update_expense, name='add_expense'),
    path('group/<int:group_id>/add_member/', views.add_member, name='add_member'),
    path('<int:group_id>/accept_invitation/<uuid:token>/', views.accept_invitation, name='accept_invitation'),
    path('join/', views.join_group, name='join_group'),


]