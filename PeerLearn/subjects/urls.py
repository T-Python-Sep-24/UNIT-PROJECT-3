from django.urls import path
from . import views

app_name = "subjects"

urlpatterns = [
    path("all/", views.all_subjects_view, name="all_subjects_view"),
    path("new/", views.new_subject_view, name="new_subject_view"),
    path("update/<subject_id>/", views.update_subject_view, name="update_subject_view"),    
    path("details/<subject_id>/", views.details_subject_view, name="details_subject_view"),
    path("delete/<brand_id>/", views.delete_subject_view, name="delete_subject_view"),    
]