from django.shortcuts import render ,redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from .models import IndividualUser , User 

# Create your views here.


def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username,password=password)

        if user is not None:

            login(request,user)
            messages.success(request, 'Login successful! Welcome')
            return redirect('main:home_view')
        
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'accounts/login.html')


    return render(request,'accounts/login.html')

def register_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('accounts:register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('accounts:register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        print("Success: Account created successfully.")
        return redirect('accounts:login') 
    
    return render(request, 'accounts/registration.html')
    
def logout_view(request):

    logout(request)  
    messages.success(request, "You have logged out successfully.")
    return redirect('main:home_view') 