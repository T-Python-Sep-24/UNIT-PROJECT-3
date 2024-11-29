from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.models import User
# Create your views here.


def project_view(request:HttpRequest):
     projects = Project.objects.all()  # جلب جميع المشاريع
     return render(request, 'main/project.html', {'projects': projects})

        
   




def dashboard_view(request:HttpRequest):
    return render(request,"main/dashboard.html")







