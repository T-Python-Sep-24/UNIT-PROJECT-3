from django.urls import path
from . import views

from .views import claude_test

app_name = "flashcards"

urlpatterns = [
    path("all/", views.all_flashcards_view, name="all_flashcards_view"),
    path("new/", views.new_flashcard_view, name="new_flashcard_view"),
    path("details/<flashcard_id>/", views.details_flashcard_view, name="details_flashcard_view"),
    path("delete/<flashcard_id>/", views.delete_flashcard_view, name="delete_flashcard_view"),
    path("<flashcard_id>", views.add_review_view, name="add_review_view"),
    path("generate/", views.generate_view, name="generate_view"),
    path('claude_test/', claude_test, name='claude_test'),
    
    # path("upload/", views.upload_pdf_view, name="upload_pdf_view"),
]