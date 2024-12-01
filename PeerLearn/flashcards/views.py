from django.shortcuts import render, redirect
from django.http import HttpRequest
from subjects.models import Subject
from .models import Flashcard, Review
from .forms import FlashcardForm
from django.contrib import messages
from PIL import Image
import pytesseract
import os
from django.conf import settings


# Create your views here.
def all_flashcards_view(request: HttpRequest):
    # subjects = Subject.objects.all()
    # flashcards = Flashcard.objects.all()
    if "search" in request.GET and len(request.GET["search"]) >= 1:
        flashcards = flashcards.filter(name__contains=request.GET["search"])
    if "subject" in request.GET and len(request.GET["subject"]) >= 1:
        # ForeignKey: use <fieldname>_id. (field stores the primary key of the related model)
        # Get all flashcards with subject specific ID 
        flashcards = flashcards.filter(subject_id=request.GET["subject"])

    context = {"flashcards": flashcards, "subjects": subjects}    

    return render(request, "flashcards/all.html", context)


def details_flashcard_view(request: HttpRequest, flashcard_id: int):
    flashcard = Flashcard.objects.get(pk=flashcard_id)
    context = {"flashcard": flashcard}

    return render(request, "flashcards/details.html", context)


def new_flashcard_view(request: HttpRequest):
    # Limit acces to members
    if not request.user.is_authenticated:
        messages.error(request, "This operation requires members account","alert-danger")
        return redirect("accounts:sign_in")

    subjects = Subject.objects.all()
    context = {"subjects": subjects}

    if request.method == "POST":
        flashcard_form = FlashcardForm(request.POST, request.FILES)
        if flashcard_form.is_valid():
            flashcard_form.save()
            messages.success(request, "Flashcard created successfully!", "alert-success")
            return redirect("flashcards:all_flashcards_view")
        else:
            print("form error: ", flashcard_form.errors)
            messages.error(request, "Error creating flashcard. Please try again later", "alert-warning")

    return render(request, "flashcards/new.html", context)


def delete_flashcard_view(request: HttpRequest, flashcard_id: int):
    # Limit acces to admin
    if not request.user.is_superuser:
        messages.error(request, "This operation requires admin account","alert-danger")
        return redirect("accounts:sign_in")

    flashcard = Flashcard.objects.get(pk=flashcard_id)
    flashcard.delete()
    messages.success(request, "Flashcard deleted successfully!", "alert-success")
    
    return redirect("flashcards:all_flashcards_view")

def upload_pdf_view(request: HttpRequest):
    img_path = os.path.join(settings.MEDIA_ROOT, 'images', 'simple.png')
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)

    print(text)

    return redirect("main:home_view")