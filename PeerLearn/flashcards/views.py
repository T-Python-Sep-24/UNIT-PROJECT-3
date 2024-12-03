from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from .models import Flashcard, TestAttempt
from subjects.models import Subject
import os
import requests
from .models import Flashcard, Review
from .forms import FlashcardForm
from utils.pdf_utils import extract_text_with_pymupdf, extract_text_with_ocr, has_meaningful_text
from utils.api_utils import process_extracted_text
from anthropic import Anthropic



# Create your views here.
def all_flashcards_view(request: HttpRequest):
    subjects = Subject.objects.all()
    flashcards = Flashcard.objects.all()
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


def tests_details_view(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view your tests", "alert-danger")
        return redirect("accounts:sign_in")
    
    # Get all test attempts for the current user, ordered by latest first
    test_attempts = TestAttempt.objects.filter(user=request.user).select_related('flashcard')
    
    context = {
        "test_attempts": test_attempts
    }
    
    return render(request, "flashcards/tests_details.html", context)


def test_flashcard_view(request: HttpRequest, flashcard_id: int):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to take tests", "alert-danger")
        return redirect("accounts:sign_in")
        
    flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
    
    if request.method == "POST":
        # Calculate score
        score = 0
        questions = flashcard.test_json.get('questions', [])
        total_questions = len(questions)
        
        # Check each answer
        for i, question in enumerate(questions):
            user_answer = request.POST.get(f'question_{i}')
            if user_answer:
                # Check if the selected answer is correct
                is_correct = any(
                    opt['is_correct'] 
                    for opt in question['options'] 
                    if str(opt['option']) == str(user_answer)
                )
                if is_correct:
                    score += 1
        
        # Save the attempt
        TestAttempt.objects.create(
            user=request.user,
            flashcard=flashcard,
            score=score,
            max_score=total_questions
        )
        
        # Show success message
        messages.success(
            request, 
            f"Test completed! Your score: {score}/{total_questions}",
            "alert-success"
        )
        
        return redirect('flashcards:details_flashcard_view', flashcard_id=flashcard_id)
    
    return render(request, "flashcards/test.html", {"flashcard": flashcard})


def new_flashcard_view(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.error(request, "This operation requires members account", "alert-danger")
        return redirect("accounts:sign_in")

    subjects = Subject.objects.all()
    context = {"subjects": subjects}

    if request.method == "POST":
        flashcard_form = FlashcardForm(request.POST, request.FILES)
        if flashcard_form.is_valid():
            try:
                # Wrap all database operations in a transaction
                with transaction.atomic():
                    # Don't save the form immediately, get an unsaved instance
                    flashcard = flashcard_form.save(commit=False)
                    
                    # Handle the PDF file
                    pdf_file = request.FILES['pdf']
                    # Save temporarily
                    temp_path = default_storage.save(
                        f'temp/{pdf_file.name}', 
                        pdf_file
                    )
                    
                    try:
                        # Get the full path
                        file_path = default_storage.path(temp_path)
                        
                        # Extract text from PDF
                        extracted_text = extract_text_with_pymupdf(file_path)
                        
                        if not extracted_text:
                            extracted_text = extract_text_with_ocr(file_path)
                        
                        if not extracted_text:
                            raise ValueError("Could not extract text from PDF")
                        
                        # Generate flashcards and test using Claude API
                        flashcards_json, test_json = process_extracted_text(extracted_text)
                        
                        if not flashcards_json or not test_json:
                            raise ValueError("Could not generate learning materials")
                        
                        # Set all the fields
                        flashcard.extracted_text = extracted_text
                        flashcard.flashcard_json = flashcards_json
                        flashcard.test_json = test_json
                        
                        # Save the flashcard only if everything succeeded
                        flashcard.save()
                        
                    finally:
                        # Clean up the temporary file
                        if temp_path:
                            default_storage.delete(temp_path)
                    
                messages.success(request, "Flashcard created successfully with learning materials!", "alert-success")
                return redirect("flashcards:all_flashcards_view")
                
            except ValueError as e:
                messages.error(request, str(e), "alert-danger")
            except Exception as e:
                print(f"Error processing flashcard: {str(e)}")
                messages.error(request, "Error processing flashcard. Please try again.", "alert-danger")
        else:
            print("Form error: ", flashcard_form.errors)
            messages.error(request, "Error creating flashcard. Please check your inputs.", "alert-warning")

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


def add_review_view(request:HttpRequest, flashcard_id):
    if not request.user.is_authenticated:
        messages.error(request, "Only registered user can add review","alert-danger")
        return redirect("accounts:sign_in")

    if request.method == "POST":
        flashcard_object = Flashcard.objects.get(pk=flashcard_id)
        new_review = Review(flashcard=flashcard_object,user=request.user,comment=request.POST["comment"],rating=request.POST["rating"])
        new_review.save()

        messages.success(request, "Added Review Successfully", "alert-success")

    return redirect("flashcards:details_flashcard_view", flashcard_id=flashcard_id)



def upload_pdf_view(request, start_page=0, end_page=10):
    """
    Django view to process and extract text from a user-specified range of PDF pages.
    """
    pdf_path = os.path.join(settings.MEDIA_ROOT, "pdfs", "test_Django_Admin.pdf")

    # Extract text using PyMuPDF (for text-based PDFs)
    text_data = extract_text_with_pymupdf(pdf_path, start_page=start_page, end_page=end_page)

    # Fall back to OCR if text extraction fails (for scanned or image-based PDFs)
    if not has_meaningful_text(text_data):
        print("[INFO] No meaningful text found with PyMuPDF. Falling back to OCR.")
        text_data = extract_text_with_ocr(pdf_path, start_page=start_page, end_page=end_page)

    if text_data:
        print("[INFO] Final Extracted Text:\n", text_data)
    else:
        print("[ERROR] No text could be extracted from the specified PDF pages.")

    return redirect("main:home_view")


def claude_test(request):
    """
    Basic view to test Claude API functionality with extracted text.
    Returns generated flashcards and test questions.
    """
    if request.method == 'POST':
        try:
            # Get extracted text from request
            extracted_text = request.POST.get('extracted_text', '')
            
            if not extracted_text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No text provided'
                })
            
            # Generate materials using Claude API
            flashcards_json, test_json = process_extracted_text(extracted_text)
            
            if flashcards_json and test_json:
                # Both JSONs are valid, you can add your logic here:
                # - Save to database
                # - Process further
                # - Add user attribution
                # - Add metadata
                # - etc.
                
                return JsonResponse({
                    'status': 'success',
                    'data': {
                        'flashcards': flashcards_json,
                        'test': test_json
                    }
                })
            
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to generate content'
            })
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    # For GET request, just render the template
    return render(request, 'flashcards/claude_test.html')