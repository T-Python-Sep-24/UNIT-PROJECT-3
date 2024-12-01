from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employee_leave.models import LeaveRequest
from django.contrib.auth.models import User
from .forms import UserCreationForm
from .forms import EditUserForm
from django.contrib.auth.models import User, Group
from django.db.models import Q
from employee_leave.models import Profile
from .forms import ManagerCreationForm
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from .forms import EditManagerForm
@login_required
def hr_dashboard(request):
    status_filter = request.GET.get('status', '')
    leave_requests = LeaveRequest.objects.all()
    if status_filter:
        leave_requests = leave_requests.filter(status=status_filter).order_by('-updated_at')[:3].select_related('employee', 'employee__profile', 'employee__profile__manager')

    pending_leaves = leave_requests.filter(status='pending')
    leave_requests = LeaveRequest.objects.filter(
        sent_to_hr=True,
        status__in=['pending', 'manager_approved']
    ).order_by('-updated_at')[:3].select_related('employee', 'employee__profile', 'employee__profile__manager')

    for leave in leave_requests:
        print(f"Employee: {leave.employee.get_full_name}, Manager: {leave.employee.profile.manager}")

    last_approved_leaves = LeaveRequest.objects.filter(
        status='approved_by_hr'
    ).order_by('-updated_at')[:3]

    rejected_leaves = LeaveRequest.objects.filter(
        status='rejected_by_hr'
    ).order_by('-updated_at')[:3]

    context = {
        'pending_leaves':pending_leaves,
        'leave_requests': leave_requests,
        'last_approved_leaves': last_approved_leaves,
        'rejected_leaves': rejected_leaves,
    }

    return render(request, 'hr_leave_management/dashboard.html', context)

@login_required
def approve_reject_leave(request, request_id):
    if request.user.is_staff:
        leave_request = get_object_or_404(LeaveRequest, id=request_id)

        if request.method == 'POST':
            action = request.POST.get('action')
            reason = request.POST.get('reason', '')

            if action == 'approve':
                leave_request.status = 'approved_by_hr'
                leave_request.hr_reason = reason
                leave_request.save()
                #if leave_request.employee.profile.email:  
                    #subject = f"Your Leave Request has been Approved"
                    #message = f"Dear {leave_request.employee.get_full_name()},\n\nYour leave request has been approved by HR.\n\nLeave Type: {leave_request.leave_type}\nStart Date: {leave_request.start_date}\nEnd Date: {leave_request.end_date}\n\nHR's Reason: {leave_request.hr_reason}\n\nEnjoy your leave!"

                    #from_email = settings.DEFAULT_FROM_EMAIL  
                    #recipient_list = [leave_request.employee.profile.email] 

                    #send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "Leave request approved successfully.")

            elif action == 'reject':
                leave_request.status = 'rejected_by_hr'
                leave_request.hr_reason = reason
                leave_request.save()
                messages.success(request, "Leave request rejected.")

            return redirect('hr_leave_management:hr_dashboard')

        return render(request, 'hr_leave_management/approve_reject_leave.html', {'leave_request': leave_request})

    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('hr_leave_management:hr_dashboard')

@login_required
def leave_requests(request):
    search_query = request.GET.get('search_query', '')
    status_filter = request.GET.get('status', '')

    leave_requests = LeaveRequest.objects.all()

    if search_query:
        leave_requests = leave_requests.filter(
            Q(employee__first_name__icontains=search_query) |
            Q(employee__last_name__icontains=search_query) |
            Q(employee__email__icontains=search_query) |
            Q(employee__username__icontains=search_query)
        )

    if status_filter:
        leave_requests = leave_requests.filter(status=status_filter)

    pending_leaves = leave_requests.filter(status='pending')
    approved_leaves = leave_requests.filter(status='approved_by_hr')
    rejected_leaves = leave_requests.filter(status='rejected_by_hr')

    paginator_pending = Paginator(pending_leaves, 6)
    paginator_approved = Paginator(approved_leaves, 6)
    paginator_rejected = Paginator(rejected_leaves, 6)

    page_pending = request.GET.get('page_pending')
    page_approved = request.GET.get('page_approved')
    page_rejected = request.GET.get('page_rejected')

    page_obj_pending = paginator_pending.get_page(page_pending)
    page_obj_approved = paginator_approved.get_page(page_approved)
    page_obj_rejected = paginator_rejected.get_page(page_rejected)

    context = {
        'pending_leaves': page_obj_pending,
        'approved_leaves': page_obj_approved,
        'rejected_leaves': page_obj_rejected,
        'search_query': search_query,
        'status': status_filter,
    }

    return render(request, 'hr_leave_management/leave_requests.html', context)

@login_required
def add_new_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has been created successfully!')
            return redirect('hr_leave_management:hr_dashboard')
        else:
            print(form.errors)  
            messages.error(request, 'There was an error creating the user. Please check the form and try again.')
    else:
        form = UserCreationForm()

    return render(request, 'hr_leave_management/add_user.html', {'form': form})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user != user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to edit this user.")
        return redirect('main:welcome')

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User information updated successfully.")
            return redirect('hr_leave_management:user_list')
    else:
        form = EditUserForm(instance=user)

    return render(request, 'hr_leave_management/edit_user.html', {'form': form})

def user_list(request):
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', None)

    users = User.objects.all()

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if role_filter:
        users = users.filter(groups__name=role_filter)

    users = users.exclude(groups__name="HR")

    user_data = []
    for user in users:
        try:
            profile = Profile.objects.get(user=user)
            user_data.append({
                'user': user,
                'manager': profile.manager,
            })
        except Profile.DoesNotExist:
            user_data.append({
                'user': user,
                'manager': None,
            })
    
    groups = Group.objects.exclude(name="HR")

    return render(request, 'hr_leave_management/user_list.html', {
        'user_data': user_data,
        'search_query': search_query,
        'groups': groups,
        'role_filter': role_filter
    })

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user != user:
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('hr_leave_management:user_list')

    messages.error(request, "You cannot delete your own account.")
    return redirect('hr_leave_management:user_list')

def add_manager(request):
    if request.method == 'POST':
        form = ManagerCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('hr_leave_management:user_list')  
        else:
            print(form.errors)  
    else:
        form = ManagerCreationForm()

    return render(request, 'hr_leave_management/add_manager.html', {
        'form': form
    })

def edit_manager(request, user_id):
    user = get_object_or_404(User, pk=user_id)  

    if request.method == 'POST':
        form = EditManagerForm(request.POST, instance=user) 
        if form.is_valid():
            form.save()  
            return redirect('hr_leave_management:user_list') 
    else:
        form = EditManagerForm(instance=user) 

    return render(request, 'hr_leave_management/edit_manager.html', {
        'form': form,
        'user': user
    })