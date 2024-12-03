from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
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


def generate_view(request):
    print(f"\n####### Inside generate view ########\n")    
    # Example extracted text (this will be dynamic in a real app)
    extracted_text = """
     Django Admin
ﻋﻦ Model ب اﻟﺨﺎﺻﺔ اﻟﺒﻴﺎﻧﺎت وﺗﻌﺪﻳﻞ إﻧﺸﺎء ﻓﻲ ﻳﺴﺎﻋﺪ Admin ب ﺧﺎﺻﺔ واﺟﻬﺔ Django وﻓﺮ
Superuser إﻧﺸﺎء ﻃﺮﻳﻖ
ﻟﺪﻳﻨﺎ اﻟﺘﻄﺒﻴﻘﺎت أﺣﺪ أن ﻻﺣﻆ ،settings.py ﻣﻠﻒ ﻋﲆ ﺑﺎﻟﺪﺧﻮل ﻗﻢ ،Superuser ﺑﺈﻧﺸﺎء اﻟﺒﺪء ﻗﺒﻞ
Admin ﺗﻄﺒﻴﻖ ﻫﻮ
Admin path وﺟﻮد ﻧﻼﺣﻆ urls.py ﻣﻠﻒ ﻓﺘﺢ ﻋﻨﺪ وأﻳﻀﺎ
 
 
1
2
3
4
5
اﻷواﻣﺮ ﺑﻜﺘﺎﺑﺔ وﻧﻘﻮم  Admin اﻟـ ﻓﻲ اﺿﺎﻓﺘﻪ ﻧﺮﻳﺪ اﻟﺬي ﺑﺎﻟﺘﻄﺒﻴﻖ اﻟﺨﺎص admin.py ﻣﻠﻒ ﺑﻔﺘﺢ ﻧﻘﻮم
:اﻟﺘﺎﻟﻴﺔ
from django.contrib import admin
from .models import Movies_Info
admin.site.register(Movies_Info)
:ﺑﺎﻟﺘﺎﻟﻲ ﻗﻤﻨﺎ اﻟﺴﺎﺑﻘﺔ اﻷﺳﻄﺮ ﻓﻲ
 .Movies_Info, Publisher, Contributor, MovieContributor, Review ل import ﻋﻤﻞ
.Admin ﻟﺘﻄﺒﻴﻖ ﻣﺘﺎﺣﺔ models ﺑﺠﻌﻞ ﺗﺴﺎﻋﺪ وﻫﻲ register method اﺳﺘﺨﺪام
:اﻷواﻣﺮ ﺑﺘﻨﻔﻴﺬ ﻧﻘﻮم
python manage.py createsuperuser
.اﻷﻣﺮ ﻛﺘﺎﺑﺔ ﺛﻢ ،ﻧﺮﻳﺪ اﻟﺬي password و email و username ﺑﺈدﺧﺎل  ﻧﻘﻮم ﺛﻢ
python manage.py runserver
(http://127.0.0.1:8000/admin) اﻟﺘﺎﻟﻲ اﻟﺮاﺑﻂ ﻋﲆ ﺑﺎﻟﺪﺧﻮل ﻧﻘﻮم
أو إﺿﺎﻓﺔ وﻳﻤﻜﻦ أﺿﻔﻨﺎ اﻟﺘﻲ Models ﺟﻤﻴﻊ ﻇﻬﻮر ﻧﻼﺣﻆ ﺳﻮف admin ﺻﻔﺤﺔ ﻋﲆ اﻟﺪﺧﻮل ﺑﻌﺪ اﻵن
.اﻟﺒﻴﺎﻧﺎت ﺗﻌﺪﻳﻞ
1
2
3
4
ﻣﻌﻠﻮﻣﺎت ﻋﺮض ﻧﺴﺘﻄﻴﻊ ﺑﺤﻴﺚ Admin ﻟﻤﻮﻗﻊ (customization) ﺗﺨﺼﻴﺺ ﻋﻤﻞ ﻧﺴﺘﻄﻴﻊ ﺣﺘﻰ
ﺑﺤﻴﺚ ،list_display attribute ﻃﺮﻳﻖ ﻋﻦ ذﻟﻚ ﺗﻨﻔﻴﺬ ﻳﻤﻜﻦ ﻣﻌﻠﻮﻣﺎﺗﻪ ﻳﺤﺘﻮي ﻛﺠﺪول Publisher
:اﻟﺘﺎﻟﻲ ﺗﻌﺪﻳﻞ ﺛﻢ admin.py ﻣﻠﻒ ﻋﲆ ﺑﺎﻟﺪﺧﻮل ﻧﻘﻮم
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'email')
admin.site.register(Publisher, PublisherAdmin)
class PublisherAdmin ﻛﺘﺎﺑﺔ
 
Admin واﺟﻬﺎت ﺗﺨﺼﻴﺺ
list_display ﺑﺎﺳﺘﺨﺪام Admin واﺟﻬﺎت ﺗﺨﺼﻴﺺ
    """  # Placeholder for your actual OCR extracted text

    # Call the utility function to get flashcards and test data
    result = generate_flashcards_and_test_from_text(extracted_text)

    if isinstance(result, dict) and 'error' in result:
        # If there is an error, log the error and show the message to the user
        print(f"\n####### error from view ########\n")
        print(f"Error Details: {result['error']}")
        messages.error(request, f"Error: {result['error']}")
        return redirect('main:home_view')

    # If everything went well, you can store the flashcards/test data or further process it
    print("######### result #########\n")
    print(f"type: {result}\n")
    print(result)

    # Success message and redirect to flashcards home view
    messages.success(request, "Flashcards and test data have been successfully generated!")

    return redirect('main:home_view')



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