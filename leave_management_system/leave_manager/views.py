from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employee_leave.models import LeaveRequest

@login_required
def manager_leave_requests(request):
    employee_leaves = LeaveRequest.objects.filter(manager=request.user).order_by('-start_date')
    pending_leaves = employee_leaves.filter(status='pending')
    approved_leaves = employee_leaves.filter(status='manager_approved')
    rejected_leaves_by_manager = employee_leaves.filter(status='rejected')
    rejected_leaves_by_hr = employee_leaves.filter(status='rejected_by_hr')
    hr_approved_leaves = employee_leaves.filter(status='approved_by_hr')

    context = {
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'rejected_leaves_by_manager': rejected_leaves_by_manager,
        'rejected_leaves_by_hr': rejected_leaves_by_hr,
        'hr_approved_leaves': hr_approved_leaves,
    }

    return render(request, 'leave_manager/manager_leave_requests.html', context)

@login_required
def approve_or_reject_leave(request, leave_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)

    if leave_request.manager != request.user:
        messages.error(request, "You are not authorized to approve or reject this leave request.")
        return redirect('leave_manager:manager_leave_requests')

    if request.method == "POST":
        action = request.POST.get('action')
        reason = request.POST.get('reason')

        if action == 'approve':
            leave_request.status = 'manager_approved'
            leave_request.manager_reason = reason
            leave_request.sent_to_hr = True
            leave_request.save()

            messages.success(request, f"Leave request from {leave_request.employee.get_full_name()} has been sent to HR for final approval.")
            return redirect('leave_manager:manager_leave_requests')

        elif action == 'reject':
            leave_request.status = 'rejected'
            leave_request.manager_reason = reason
            leave_request.save()
            messages.success(request, f"Leave request from {leave_request.employee.get_full_name()} has been rejected.")
            return redirect('leave_manager:manager_leave_requests')

    context = {
        'leave_request': leave_request,
    }
    return render(request, 'leave_manager/approve_or_reject_leave.html', context)
