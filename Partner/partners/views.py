from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Request,Partner,Message,RoomMember
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random
import time
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def start_chat_room(request):
     return render(request,'partners/chat_room.html')     
def getToken(request):
    appId = "a0434689a62a469b9bbbad6898460ef6"
    appCertificate = "21ada07cbb94421295618e16ed658198"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)


def new_request_view(request:HttpRequest,sender_id,recevier_id):
    try: 
        recevier=User.objects.get(pk=recevier_id)
        if not request.user.is_authenticated and request.user != request.user and recevier.profile.role != 'editor':
            messages.warning(request,"only rigisted user can send requests","alert-warning")
            return redirect("accounts:sign_in") 
     
        sender=User.objects.get(pk=sender_id)
        
        request_obj=Request.objects.filter(sender=sender,receiver=recevier)
        if not request_obj:
            if request.method == "POST":
                scheduled_at = request.POST.get("scheduled_at")
                new_request=Request(sender=sender,receiver=recevier,scheduled_at=scheduled_at)
                new_request.save()
        else:
            request_obj.delete()
        return redirect("accounts:user_profile_view",user_name=recevier.username)
    except Exception as e:
            print(e)
            return redirect("main:home_view")
   
def delete_request_view(request:HttpRequest,sender_id,recevier_id):
    try:
        recevier=User.objects.get(pk=recevier_id)

        if not request.user.is_authenticated and request.user != request.user and recevier.profile.role != 'editor':
            messages.warning(request,"only rigisted user can delete requests","alert-warning")
            return redirect("accounts:sign_in") 
        sender=User.objects.get(pk=sender_id)
        request=Request.objects.get(sender=sender,receiver=recevier)
        request.delete() 
        return redirect("accounts:user_profile_view",user_name=recevier.username)
    except Exception as e:
            print(e)
            return redirect("main:home_view")


def new_partner_view(request:HttpRequest,user_id,partner_id):
      if not request.user.is_authenticated and request.user != request.user:
            messages.warning(request,"only rigisted user can make partnes","alert-warning")
            return redirect("accounts:sign_in") 
      
      try:
         with transaction.atomic():
            request_obj=Request.objects.get(sender=partner_id,receiver=user_id)
            request_obj.status = 'accepted'
            request_obj.save()
            self_user=User.objects.get(pk=user_id)
            partner=User.objects.get(pk=partner_id)
            partner_rel=Partner(user=self_user,partner=partner,scheduled_at=request_obj.scheduled_at)
            partner_rel.save()
         return redirect("accounts:user_profile_view",user_name=self_user.username)

      except Exception as e:
            print(e)
            return redirect("main:home_view")
      
def delete_partner_view(request:HttpRequest,user_id,partner_id):
      if not request.user.is_authenticated and request.user != request.user:
            messages.warning(request,"only rigisted user can delete partnes","alert-warning")
            return redirect("accounts:sign_in") 
      
      try:
         with transaction.atomic():
            request_obj=Request.objects.get(sender=partner_id,receiver=user_id)
            request_obj.delete()
            self_user=User.objects.get(pk=user_id)
            partner=User.objects.get(pk=partner_id)
            partner_rel=Partner.objects.filter(user=self_user,partner=partner)
            partner_rel.delete()
         return redirect("accounts:user_profile_view",user_name=self_user.username)

      except Exception as e:
            print(e)
            return redirect("main:home_view")
      

