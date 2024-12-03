from django.shortcuts import render
from django.http import HttpRequest
from flashcards.models import Flashcard 

# Create your views here.
def home_view(request: HttpRequest):
    flashcards = Flashcard.objects.all().order_by("-id")[0:4]
    context = {"flashcards": flashcards}

    if request.user.is_authenticated:
        print("user is authenticated")
    else:
        print("user isn't logged in")

    return render(request, "main/index.html", context)