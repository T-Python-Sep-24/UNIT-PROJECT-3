from django.urls import path
from . import views

app_name = "subjects"

urlpatterns = [
    path("all/", views.all_subjects_view, name="all_subjects_view"),
    path("new/", views.new_subject_view, name="new_subject_view"),
    path("details/<subject_id>/", views.details_subject_view, name="details_subject_view"),
]