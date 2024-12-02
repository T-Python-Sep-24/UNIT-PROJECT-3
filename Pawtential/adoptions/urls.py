from django.urls import path
from . import views

app_name = 'adoptions'

urlpatterns = [
    path('request/<pet_id>/', views.request_adoption, name='request_adoption'),
    path('adoption_request/<request_id>/<str:action>/', views.handle_adoption_request, name='handle_adoption_request'),
]


