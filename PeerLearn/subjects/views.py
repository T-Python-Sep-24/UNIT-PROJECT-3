from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Subject
from flashcards.models import Flashcard
from .forms import SubjectForm
from django.contrib import messages

# Create your views here.
def all_subjects_view(request: HttpRequest):
    subjects = Subject.objects.all()
    if "search" in request.GET:
        subjects = subjects.filter(name__contains=request.GET["search"])

    context = {"subjects": subjects}

    return render(request, "subjects/all.html", context)


def new_subject_view(request: HttpRequest):
    # Limit acces to admin
    if not request.user.is_superuser:
        messages.error(request, "This operation requires admin account","alert-danger")
        return redirect("accounts:sign_in")

    if request.method == "POST":
        subject_form = SubjectForm(request.POST, request.FILES)
        if subject_form.is_valid():
            subject_form.save()
            return redirect("subjects:all_subjects_view")
        else:
            print("form error: ", subject_form.errors)

    return render(request, "subjects/new.html")


def update_subject_view(request: HttpRequest, subject_id: int):
    # Limit acces to admin
    if not request.user.is_superuser:
        messages.error(request, "This operation requires admin account","alert-danger")
        return redirect("accounts:sign_in")

    subject = Subject.objects.get(pk=subject_id)
    context = {"subject": subject}

    if request.method == "POST":
        # updating an existing object (car) not creating new one
        subject_form = SubjectForm(instance=subject, data=request.POST, files=request.FILES)
        if subject_form.is_valid():
            subject_form.save()
            return redirect("subjects:all_subjects_view")
        else:
            print("form error: ", subject_form.errors)

    return render(request, "subjects/update.html", context)


def details_subject_view(request: HttpRequest, subject_id: int):
    subject = Subject.objects.get(pk=subject_id)
    flashcards = Flashcard.objects.all().filter(subject=subject)
    context = {"subject": subject, "flashcards": flashcards}

    return render(request, "subjects/details.html", context)


def delete_subject_view(request: HttpRequest, subject_id: int):
    # Limit acces to admin
    if not request.user.is_superuser:
        messages.error(request, "This operation requires admin account","alert-danger")
        return redirect("accounts:sign_in")

    subject = Subject.objects.get(pk=subject_id)
    subject.delete()

    return redirect("subjects:all_subjects_view")

