from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import ContactSubmission  

def contact_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
       
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact_submission = ContactSubmission(
            name=name,
            email=email,
            message=message,
           
        )
        contact_submission.save()

        messages.success(request, "Your message has been sent successfully!")

        return redirect('main_app:home_view')  

    return render(request, 'contact_app/contact_form.html')  
