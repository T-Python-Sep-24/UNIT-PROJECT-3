from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Request,Partner,Message,Session
from django.contrib.auth.models import User
# Create your views here.



def new_request_view(request:HttpRequest,sender_id,recevier_id):
    if not request.user.is_authenticated and request.user != request.user:
            messages.warning(request,"only rigisted user can send requests","alert-warning")
            return redirect("accounts:sign_in") 
    try:
        sender=User.objects.get(pk=sender_id)
        recevier=User.objects.get(pk=recevier_id)
        request=Request.objects.filter(sender=sender,receiver=recevier)
        if not request:
            new_request=Request(sender=sender,receiver=recevier)
            new_request.save()
        else:
            request.delete()
        return redirect("accounts:user_profile_view",user_name=recevier.username)
    except Exception as e:
            print(e)
   