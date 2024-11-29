from django.urls import path
from . import views

urlpatterns = [
    path('add_expense/', views.add_expense, name='add-expense'),
    path('add_budget/', views.add_budget, name='add-budget'),
    path('add_salary/', views.add_salary, name='add_salary'),  

]