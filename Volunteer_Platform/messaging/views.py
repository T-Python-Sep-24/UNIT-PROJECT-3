# messaging/views.py
from django.shortcuts import render, redirect
from .models import Message
from django.contrib.auth.models import User

def inbox(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'messaging/inbox.html', {'messages': messages})

def send_message(request, receiver_id):
    if request.method == 'POST':
        receiver = User.objects.get(pk=receiver_id)
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('inbox')
    return render(request, 'messaging/send_message.html', {'receiver_id': receiver_id})


def review_list(request):
    return render(request, 'reviews/review_list.html')  # Placeholder template

