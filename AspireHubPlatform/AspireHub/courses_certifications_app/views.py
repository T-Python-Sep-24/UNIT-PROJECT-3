from django.shortcuts import render , redirect
from django.http import HttpRequest , HttpResponse
from .models import Course , Certification
from django.contrib import messages

# Create your views here.

def add_course_view(request:HttpRequest):
        if request.method == "POST":
           new_course=Course(
           title = request.POST["title"],
           description = request.POST["description"],
           image=request.FILES["image"],
           duration = request.POST["duration"],
           prerequisites= request.POST["prerequisites"],
           
       )
           new_course.save()
           return redirect('courses_certifications_app:lists_courses_certifications_view')
        return render(request, "courses_certifications_app/add_courses.html")


def add_certification_view(request:HttpRequest):
        if request.method == "POST":
           new_certification=Certification(
           name = request.POST["name"],
           description = request.POST["description"],
           image=request.FILES["image"],
           classification = request.POST["classification"],
           cost= request.POST["cost"],
           estimated_study_time= request.POST["estimated_study_time"],
           
       )
           new_certification.save()
           return redirect('courses_certifications_app:lists_courses_certifications_view')
        return render(request, "courses_certifications_app/add_certification.html")

def lists_courses_certifications_view(request:HttpRequest):
    courses = Course.objects.all()
    certifications = Certification.objects.all()
    return render(request,'courses_certifications_app/lists_courses_certifications.html' ,{'courses':courses, 'certifications':certifications})


def details_course_view(request:HttpRequest , course_id:int):
    course= Course.objects.get(pk=course_id)
    return render(request, "courses_certifications_app/details_course.html", {'course': course})

def details_certification_view(request:HttpRequest ,certification_id:int):
    certification= Certification.objects.get(pk= certification_id)
    return render(request, "courses_certifications_app/details_certification.html", {'certification':certification })

def update_course_view(request:HttpRequest,course_id:int):
    course= Course.objects.get(pk=course_id)
    if request.method == "POST":
      course.title = request.POST["title"]
      course.description = request.POST["description"]
      course.duration = request.POST["duration"]
      course.prerequisites = request.POST["prerequisites"]
      if "image" in request.FILES: course.image = request.FILES["image"]
      course.save()
      return redirect('courses_certifications_app:lists_courses_certifications_view',course_id=course.id)
    return render(request, 'courses_certifications_app/update_course.html',{'course':course})


def update_certification_view(request:HttpRequest,certification_id:int):
    certification= Certification.objects.get(pk=certification_id)
    if request.method == "POST":
      certification.name  = request.POST["name"]
      certification.description = request.POST["description"]
      certification.classification = request.POST["classification"]
      certification.estimated_study_time = request.POST["estimated_study_time"]
      if "image" in request.FILES: certification.image = request.FILES["image"]
      certification.save()
      return redirect('courses_certifications_app:lists_courses_certifications_view',certification_id= certification.id)
    return render(request, 'courses_certifications_app/update_certification.html',{'certification':certification})


def delete_course_view(request:HttpRequest,course_id:int):
    course = Course.objects.get(pk=course_id)
    messages.warning(request, f'Are you sure you want to delete the course: {course.title}? This action cannot be undone.')
    course.delete()
    messages.success(request, 'Course deleted successfully.')
    return redirect('courses_certifications_app:lists_courses_certifications_view ',{'course':course})


def delete_certification_view(request:HttpRequest,certification_id:int):
    certification = Certification.objects.get(pk=certification_id)
    messages.warning(request, f'Are you sure you want to delete the certification: {certification.name}? This action cannot be undone.')
    certification.delete()
    messages.success(request, 'Certification deleted successfully.')
    return redirect('courses_certifications_app:lists_courses_certifications_view ',{'certification':certification})