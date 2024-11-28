from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LeaveRequestForm
from .models import LeaveRequest
from django.contrib.auth.models import User

@login_required
def request_leave(request):
    if not request.user.groups.filter(name='Employee').exists():
        messages.error(request, "You do not have permission to view this page.")
        return redirect('main:welcome')

    if request.method == "POST":
        form = LeaveRequestForm(request.POST, request.FILES)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.status = 'pending'

            employee_group = request.user.groups.filter(name='Employee').first()
            if employee_group:
                try:
                    manager = User.objects.get(username='Abdullah1')
                    leave_request.manager = manager
                except User.DoesNotExist:
                    messages.error(request, "Manager 'Abdullah1' not found.")
                    return redirect('employee_leave:leave_requests')
                
            leave_request.save()
            messages.success(request, "Your leave request has been successfully submitted and is awaiting approval.")
            return redirect('employee_leave:leave_requests')
    else:
        form = LeaveRequestForm()

    return render(request, 'employee_leave/request_leave.html', {'form': form})

@login_required
def leave_requests(request):
    employee_leaves = LeaveRequest.objects.filter(employee=request.user).order_by('-start_date')

    pending_leaves = employee_leaves.filter(status='pending')
    approved_leaves = employee_leaves.filter(status='approved')
    rejected_leaves = employee_leaves.filter(status='rejected')

    context = {
        'employee_name': request.user.get_full_name(),
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'rejected_leaves': rejected_leaves,
    }

    return render(request, 'employee_leave/leave_requests.html', context)
