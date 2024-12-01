from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Contact
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime
from django.contrib import messages

from artists.models import Artist
from artPieces.models import ArtPiece

# Home View
def homeView(request: HttpRequest):
    pieces = ArtPiece.objects.all().order_by('-addedAt')[:4]
    artists = Artist.objects.all().order_by('-addedAt')[:4]
    
    return render(request, 'main/index.html', {'pieces': pieces, 'artists': artists})

#Contact us View
def contactView(request: HttpRequest):
    contactData = ContactForm()

    response = render(request, 'main/contact.html')
    
    if request.method == "POST":

        contactData = ContactForm(request.POST)
        if contactData.is_valid():
            contactData.save()

            subject = "The Gallery"
            fromEmail = settings.DEFAULT_FROM_EMAIL
            to = request.POST['email']
            htmlContent = render_to_string('main/mail/mailTemplate.html', {'reciever': request.POST['fname'], 'sentAt': datetime.strftime(datetime.now() , "%d/%m/%Y, %H:%M:%S")})
            emailMsg = EmailMessage(subject, htmlContent,  fromEmail, [to])
            emailMsg.content_subtype = "html"
            emailMsg.send()
            messages.success(request, "Your message was sent successfully. Thank you.", "alert-success") 

    return response

#All messages View
def allMessagesView(request: HttpRequest):
    messages = Contact.objects.all().order_by("-createdAt")
    response = render(request, 'main/allMessages.html', {'messages': messages})

    return response