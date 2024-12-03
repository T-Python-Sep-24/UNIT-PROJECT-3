from django.shortcuts import render, redirect
from .models import Company, Employee, Event
from django.http import HttpRequest , HttpResponse
from django.contrib import messages

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
        return redirect('events_companies_app:lists_companies_events_view')
    return render(request, "events_companies_app/add_company.html")

def add_employee_view(request:HttpRequest):
    if request.method == "POST":
        company_id = request.POST["company"]
        new_employee=Employee(
        name = request.POST["name"],
        specialty =request.POST["specialty"],
        image=request.FILES["image"],
        description =request.POST["description"],
        linkedin_link=request.POST["linkedin_link"],
        company_id=company_id   
       )
        new_employee.save()
        companies = Company.objects.all()
        return redirect('events_companies_app:details_companies_view')
    return render(request, "events_companies_app/add_employee.html",{'companies': companies})
 

def add_event_view(request:HttpRequest):
    if request.method == "POST":
        new_event = Event(
        title = request.POST["title"],
        description = request.POST["description"],
        image=request.FILES["image"],
        date= request.POST["date"],   
      )
        new_event.save()
        return redirect('events_companies_app:details_companies_view')
    return render(request, "events_companies_app/add_event.html")


def lists_companies_events_view(request:HttpRequest):
    companies = Company.objects.all()
    events = Event.objects.all()
    return render(request, 'events_companies_app/lists_companies_events.html' ,{'companies': companies, 'events':events})

def details_companies_view(request:HttpRequest , company_id:int ):
    company= Company.objects.get(pk=company_id)
    employees= Employee.objects.all()
    return render(request, "events_companies_app/details_compines.html", {'company':company , 'employees':employees})

def details_events_view(request:HttpRequest , event_id:int):
    event= Event.objects.get(pk= event_id)
    return render(request, "events_companies_app/details_events.html", {'event': event})

def update_company_view(request:HttpRequest , company_id:int):
    company= Company.objects.get(pk=company_id)
    if request.method == "POST":
     company.name = request.POST["name"]
     company.description = request.POST["description"]
     company.website = request.POST["website"]
     company.specialization = request.POST["specialization"]
     if "logo" in request.FILES:company.logo = request.FILES["logo"]
     company.save()
     return redirect('events_companies_app:details_companies_view',company_id=company.id)
    return render(request, 'events_companies_app/update_company.html',{'company':company})

def update_employee_view(request:HttpRequest,):

    return render(request, 'events_companies_app/update_employee.html')

def update_event_view(request:HttpRequest,event_id:int):
    event= Event.objects.get(pk=event_id)
    if request.method == "POST":
      event.title  = request.POST["title"]
      event.description  = request.POST["description"]
      event.date  = request.POST["date"]
      if "image" in request.FILES: event.image = request.FILES["image"]
      event.save()
      return redirect('events_companies_app:details_events_view',event_id= event.id)
    return render(request, 'events_companies_app/update_event.html',{'event':event})

def delete_company_view(request:HttpRequest,company_id:int):
    company= Company.objects.get(pk=company_id)
    messages.warning(request, f'Are you sure you want to delete the company: {company.name}? This action cannot be undone.')
    company.delete()
    messages.success(request, 'Company deleted successfully.')
    return redirect('events_companies_app:lists_companies_events_view',{'company':company})

def delete_employee_view(request:HttpRequest):
   
    return redirect('events_companies_app:details_company_employees_view')

def delete_event_view(request:HttpRequest,event_id:int):
    event = Event.objects.get(pk=event_id)
    messages.warning(request, f'Are you sure you want to delete the event: {event.title}? This action cannot be undone.')
    event.delete()
    messages.success(request, 'Event deleted successfully.')
    return redirect('events_companies_app:lists_companies_events_view',{'event':event})

   
