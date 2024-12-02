from django.shortcuts import render, get_object_or_404, redirect
from .models import Message
from .forms import MessageForm
from django.contrib.auth.decorators import login_required

@login_required
def inbox(request):
    messages = request.user.received_messages.all().order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def sent_messages(request):
    messages = request.user.sent_messages.all().order_by('-timestamp')
    return render(request, 'messaging/sent_messages.html', {'messages': messages})

@login_required
def compose_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('messaging:inbox')
    else:
        form = MessageForm()
    return render(request, 'messaging/compose_message.html', {'form': form})

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk, receiver=request.user)
    message.read = True
    message.save()
    return render(request, 'messaging/message_detail.html', {'message': message})
