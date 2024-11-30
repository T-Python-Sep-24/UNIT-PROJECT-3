from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, Employee, Event
from .form import CompanyForm, EmployeeForm, EventForm
from django.contrib import messages

def add_company_view(request):
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('events_companies_app:details_company_employees_view')
    else:
        form = CompanyForm()
    return render(request, 'add_company.html', {'form': form})
def add_employee_view(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events_companies_app:details_company_employees_view')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form, 'companies': Company.objects.all()})

def add_event_view(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('events_companies_app:events_list_view')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})

def details_company_employees_view(request):
    companies = Company.objects.all()
    return render(request, 'details_company_employees.html', {'companies': companies})

def events_list_view(request):
    events = Event.objects.all()
    return render(request, 'events_list.html', {'events': events})

def update_company_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('events_companies_app:details_company_employees_view')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'update_company.html', {'form': form, 'company': company})

def update_employee_view(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('events_companies_app:details_company_employees_view')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'update_employee.html', {'form': form, 'employee': employee, 'companies': Company.objects.all()})

def update_event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events_companies_app:events_list_view')
    else:
        form = EventForm(instance=event)
    return render(request, 'update_event.html', {'form': form, 'event': event})

def delete_company_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == "POST":
        company.delete()
        messages.success(request, f'Company "{company.name}" has been deleted successfully.')
        return redirect('events_companies_app:details_company_employees_view')
    return redirect('events_companies_app:details_company_employees_view')

def delete_employee_view(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == "POST":
        employee.delete()
        messages.success(request, f'Employee "{employee.name}" has been deleted successfully.')
        return redirect('events_companies_app:details_company_employees_view')
    return redirect('events_companies_app:details_company_employees_view')

def delete_event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        event.delete()
        messages.success(request, f'Event "{event.title}" has been deleted successfully.')
        return redirect('events_companies_app:events_list_view')
    return redirect('events_companies_app:events_list_view')
