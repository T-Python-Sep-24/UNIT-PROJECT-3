from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from leave_manager.models import LeaveRequest

def hr_dashboard(request):
    leave_requests = LeaveRequest.objects.filter(sent_to_hr=True)
    print(leave_requests)

    return render(request, 'hr_leave_management/dashboard.html', {'leave_requests': leave_requests})

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

            leave_request.employee.email_user(
                'Leave Request Update',
                f'Your leave request has been {leave_request.status}. Reason: {leave_request.hr_reason}'
            )

            return redirect('hr_leave_management:leave_requests')

        return render(request, 'hr_leave_management/approve_reject_leave.html', {'leave_request': leave_request})
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('hr_leave_management:hr_dashboard')

@login_required
def leave_requests(request):
    if request.user.is_staff:
        leave_requests = LeaveRequest.objects.filter(sent_to_hr=True, status='manager_approved')
        return render(request, 'hr_leave_management/leave_requests.html', {'leave_requests': leave_requests})
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('hr_leave_management:hr_dashboard')

@login_required
def approve_or_reject_leave(request, leave_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)

    if request.method == "POST":
        action = request.POST.get('action')
        reason = request.POST.get('reason')

        if action == 'approve':
            leave_request.status = 'manager_approved'
            leave_request.manager_reason = reason
            leave_request.sent_to_hr = True
            leave_request.save()
            messages.success(request, f"Leave request from {leave_request.employee.get_full_name()} has been sent to HR for final approval.")
            return redirect('hr_leave_management:hr_dashboard')

        elif action == 'reject':
            leave_request.status = 'rejected'
            leave_request.manager_reason = reason
            leave_request.save()
            messages.success(request, f"Leave request from {leave_request.employee.get_full_name()} has been rejected.")
            return redirect('manager_leave_requests')

    return render(request, 'employee_leave/approve_or_reject_leave.html', {'leave_request': leave_request})
