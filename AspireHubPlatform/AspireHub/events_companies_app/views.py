from django.shortcuts import render, redirect
from .models import Company, Employee, Event
from django.http import HttpRequest , HttpResponse
# from .form import CompanyForm, EmployeeForm, EventForm
# from django.contrib import messages

def add_company_view(request:HttpRequest):
    if request.method == "POST":
        new_company=Company(
        name = request.POST["name"],
        description = request.POST["description"],
        logo=request.FILES["logo"],
        website = request.POST["website"],
        specialization= request.POST["specialization"],
           
       )
        new_company.save()
    return render(request, "events_companies_app/add_company.html")

def add_employee_view(request:HttpRequest):
 
    return render(request, "events_companies_app/add_employee.html")

def add_event_view(request:HttpRequest):
    if request.method == "POST":
        new_event = Event(
        title = request.POST["title"],
        description = request.POST["description"],
        image=request.FILES["image"],
        date= request.POST["date"],   
      )
        new_event.save()
    return render(request, "events_companies_app/add_event.html")


def lists_companies_events_view(request:HttpRequest):
    companies = Company.objects.all()
    events = Event.objects.all()
    return render(request, 'events_companies_app/lists_companies_events.html' ,{'companies': companies, 'events':events})

def details_companies_view(request:HttpRequest):

    return render(request, "events_companies_app/details_compines.html")

def events_list_view(request:HttpRequest):
    return render(request, "events_companies_app/events_list.html")

def update_company_view(request:HttpRequest):

    return render(request, 'events_companies_app/update_company.html')

def update_employee_view(request:HttpRequest):

    return render(request, 'events_companies_app/update_employee.html')

def update_event_view(request:HttpRequest):

    return render(request, 'events_companies_app/update_event.html')

def delete_company_view(request:HttpRequest):
   
   return redirect('events_companies_app:details_company_employees_view')

def delete_employee_view(request:HttpRequest):
   

    return redirect('events_companies_app:details_company_employees_view')

def delete_event_view(request:HttpRequest):

    return redirect('events_companies_app:events_list_view')
