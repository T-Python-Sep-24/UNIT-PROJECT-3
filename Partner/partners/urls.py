from . import views
from django.urls import path

app_name="partners"

urlpatterns=[
    path("new/request/<sender_id>/<recevier_id>/",views.new_request_view,name="new_request_view")
]