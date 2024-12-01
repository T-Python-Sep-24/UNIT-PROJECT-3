from django.shortcuts import render, redirect
from django.http import HttpRequest
from subjects.models import Subject
from .models import Flashcard, Review
from .forms import FlashcardForm
from django.contrib import messages
import os
from django.conf import settings
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader



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
    # test extracting text from image
    img_path = os.path.join(settings.MEDIA_ROOT, "images", "simple.png")
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    print(text)

    
    # Test extracting text from pdf
    use_ocr = False
    pdf_path = os.path.join(settings.MEDIA_ROOT, "pdfs", "pdf_sample3.pdf")
    text_data = ""

    if not use_ocr:
        # Try text-based extraction first because use_ocr = False
        pdf_reader = PdfReader(pdf_path)

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            # Check if there is text extracted
            if page_text and not page_text.isspace():
                text_data += page_text

        # Print the text if text is found
        if text_data.strip():
            print("****** Printed using PdfReader ******\n", text_data)

    # Fallback to OCR for image-based PDFs, if no text was extracted
    if not text_data.strip():  
        pages = convert_from_path(pdf_path, 500)
        text_data = ""
        for page in pages:
            text_data += pytesseract.image_to_string(page) + "\n"
        print("****** Printed using OCR ******\n", text_data) 



    return redirect("main:home_view")