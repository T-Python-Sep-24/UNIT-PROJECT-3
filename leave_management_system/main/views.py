from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group


def welcome(request):
    return render(request, 'main/welcome.html')


def login_view(request, role=None):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            if role == 'employee':
                if user.groups.filter(name='Employee').exists():
                    return redirect('employee_leave:leave_requests')
                else:
                    messages.error(request, "You are not an employee.")
                    return redirect('main:welcome')

            elif role == 'manager':
                if user.groups.filter(name='Managers').exists():
                    return redirect('leave_manager:manager_leave_requests')
                else:
                    messages.error(request, "You are not a manager.")
                    return redirect('main:welcome')

            elif role == 'hr':
                if user.groups.filter(name='HR').exists():
                    return redirect('hr_leave_management:hr_dashboard')
                else:
                    messages.error(request, "You are not an HR employee.")
                    return redirect('main:welcome')

            else:
                messages.error(request, "Invalid role.")
                return redirect('main:welcome')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('main:login', {'role': role})

    else:
        return render(request, 'main/login.html', {'role': role})


def user_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('main:welcome')
