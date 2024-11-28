from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employee_leave.models import LeaveRequest
from .forms import UserCreationForm

@login_required
def hr_dashboard(request):
    leave_requests = LeaveRequest.objects.filter(sent_to_hr=True, status__in=['pending', 'manager_approved']).order_by('-start_date')[:3]
    last_approved_leave = LeaveRequest.objects.filter(status='approved_by_hr').order_by('-updated_at').first()
    rejected_leaves = LeaveRequest.objects.filter(status='rejected_by_hr').order_by('-updated_at')[:3]

    context = {
        'leave_requests': leave_requests,
        'last_approved_leave': last_approved_leave,
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
                messages.success(request, "Leave request approved successfully.")

            elif action == 'reject':
                leave_request.status = 'rejected_by_hr'
                leave_request.hr_reason = reason
                leave_request.save()
                messages.success(request, "Leave request rejected.")

            return redirect('hr_leave_management:leave_requests')

        return render(request, 'hr_leave_management/approve_reject_leave.html', {'leave_request': leave_request})
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('hr_leave_management:hr_dashboard')

@login_required
def leave_requests(request):
    leave_request = LeaveRequest.objects.filter(hr=request.user).order_by('-start_date')
    pending_leaves = leave_request.filter(status='pending')
    approved_leaves = leave_request.filter(status='approved_by_hr')
    rejected_leaves = leave_request.filter(status='rejected_by_hr')
    
    context = {
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'rejected_leaves': rejected_leaves,
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
        form = UserCreationForm()

    return render(request, 'hr_leave_management/add_user.html', {'form': form})
