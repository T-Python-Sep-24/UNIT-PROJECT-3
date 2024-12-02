from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
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
import fitz # PyMuPDF lib

def has_meaningful_text(text):
    """Check if the string contains meaningful (non-whitespace) characters."""
    return any(char.isalnum() for char in text)  # Checks for letters or numbers


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
    pdf_path = os.path.join(settings.MEDIA_ROOT, "pdfs", "pdf_sample3.pdf")
    text_data = ""

    def is_valid_text(text: str) -> bool:
        """Check if the text has meaningful, readable content."""
        return bool(text.strip() and not all(c in "\x01 \n" for c in text))

    # Try extracting text using PyMuPDF
    try:
        with fitz.open(pdf_path) as doc:
            print("******* Attempting text extraction with PyMuPDF...")
            for page_number, page in enumerate(doc, start=1):
                page_text = page.get_text("text")
                if is_valid_text(page_text):
                    print(f"****** Extracted text from page {page_number} using PyMuPDF.")
                    text_data += page_text
            if not is_valid_text(text_data):
                print("******* No meaningful text extracted using PyMuPDF.")
    except fitz.exceptions.FSError as e:
        print("******** Error opening PDF with PyMuPDF:", e)

    # Fall back to OCR if text extraction fails
    if not is_valid_text(text_data):
        print("####### No valid text found; falling back to OCR...")
        try:
            pages = convert_from_path(pdf_path, 500)
            for page_number, page in enumerate(pages, start=1):
                ocr_text = pytesseract.image_to_string(page)
                if is_valid_text(ocr_text):
                    print(f"####### Extracted text from page {page_number} using OCR.")
                    text_data += ocr_text + "\n"
        except Exception as e:
            print(f"####### Error during OCR: {e}")
            return HttpResponse("####### Error processing PDF with OCR.", status=500)

    # Debug Output
    if text_data:
        print("Final Extracted Text:\n", text_data)
    else:
        print("No text could be extracted from the PDF.")

    return redirect("main:home_view")


# first version ***************************
# def upload_pdf_view(request: HttpRequest):
    # if not use_ocr:
    #     # Try text-based extraction first because use_ocr = False
    #     pdf_reader = PdfReader(pdf_path)

    #     for page in pdf_reader.pages:
    #         page_text = page.extract_text()
    #         # Check if there is text extracted
    #         if page_text and not page_text.isspace():
    #             text_data += page_text

    #     # Print the text if text is found
    #     if text_data.strip():
    #         print("****** Printed using PdfReader ******\n", text_data)

    # Try text-based extraction with PyMuPDF first
    # try:
    #     with fitz.open(pdf_path) as doc:
    #         print("******* Opening file with PyMuPDF")
    #         for page in doc:
    #             # Extract text using get_text method
    #             page_text = page.get_text("text")
    #             print(f"Extracted text from page: {page_text.strip()}")  # Debug print
    #             if page_text.strip():  # Ensure the text is non-empty
    #                 text_data += page_text

        # # Check if meaningful text was extracted
        # if text_data.strip():  # Ensure non-whitespace text is present
        #     print("****** Printed using PdfReader ******\n", text_data)
        # else:
        #     print("******* No meaningful text extracted using PyMuPDF.")
    # except fitz.exceptions.FSError as:
    #     print("Error opening PDF with PyMuPDF")

    #     print("Error opening PDF with PyMuPDF:", e)


    # # Fallback to OCR for image-based PDFs, if no text was extracted
    # if not text_data.strip():
    #     print("######### No text found in PDF, using OCR.")
    #     pages = convert_from_path(pdf_path, 500)
    #     text_data = ""
    #     for page in pages:
    #         text_data += pytesseract.image_to_string(page) + "\n"
    #     print("######## Printed using OCR #######\n", text_data) 

    # return redirect("main:home_view")


# second version ******************

# def upload_pdf_view(request: HttpRequest):
#     # test extracting text from image
#     img_path = os.path.join(settings.MEDIA_ROOT, "images", "simple.png")
#     img = Image.open(img_path)
#     text = pytesseract.image_to_string(img)
#     print(text)

    
#     # Test extracting text from pdf
#     use_ocr = False
#     pdf_path = os.path.join(settings.MEDIA_ROOT, "pdfs", "pdf_sample3.pdf")
#     text_data = ""



#     # Try text-based extraction with PyMuPDF first updated
#     try:
#         with fitz.open(pdf_path) as doc:
#             print("******* Opening file with PyMuPDF")
#             for page_number, page in enumerate(doc, start=1):
#                 page_text = page.get_text("text")
#                 print(f"Extracted text from page {page_number}: {repr(page_text.strip())}")  # Debug print
#                 if has_meaningful_text(page_text):  # Append only if meaningful text exists
#                     text_data += page_text
#             if has_meaningful_text(text_data):
#                 print("****** Printed using PyMuPDF ******\n", text_data)
#             else:
#                 print("No meaningful text extracted using PyMuPDF.")

#     except fitz.exceptions.FSError as e:
#         print("Error opening PDF with PyMuPDF:", e)

#     # Fallback to OCR for image-based PDFs, if no meaningful text was extracted
#     if not has_meaningful_text(text_data):  
#         print("No meaningful text found in PDF, using OCR.")
#         pages = convert_from_path(pdf_path, 500)
#         text_data = ""
#         for page_number, page in enumerate(pages, start=1):
#             ocr_text = pytesseract.image_to_string(page)
#             print(f"OCR text from page {page_number}: {repr(ocr_text.strip())}")  # Debug print
#             text_data += ocr_text + "\n"
#         print("****** Printed using OCR ******\n", text_data)


#     return redirect("main:home_view")