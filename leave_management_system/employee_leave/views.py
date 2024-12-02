from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LeaveRequestForm
from .models import LeaveRequest
from django.contrib.auth.models import User
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.core.mail import send_mail
import matplotlib.pyplot as plt


@login_required
def request_leave(request):
    if not request.user.groups.filter(name='Employee').exists():
        messages.error(request, "You do not have permission to view this page.")
        return redirect('main:welcome')

    approved_by_hr_leaves = LeaveRequest.objects.filter(employee=request.user, status='approved_by_hr')
    pending_leaves = LeaveRequest.objects.filter(employee=request.user, status='pending')

    total_leave_taken = sum((leave.end_date - leave.start_date).days + 1 for leave in approved_by_hr_leaves)

    max_leave_days = 30  

    if total_leave_taken >= max_leave_days:
        messages.error(request, "You have exhausted all your leave days and cannot submit a new leave request.")
        return redirect('employee_leave:leave_requests')

    def is_leave_date_taken(start_date, end_date):
        all_leaves = approved_by_hr_leaves.union(pending_leaves)
        for leave in all_leaves:
            if (start_date <= leave.end_date and end_date >= leave.start_date):
                return True
        return False

    if request.method == "POST":
        form = LeaveRequestForm(request.POST, request.FILES)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.status = 'pending'

            try:
                leave_request.manager = request.user.profile.manager
            except AttributeError:
                leave_request.manager = None

            start_date = leave_request.start_date
            end_date = leave_request.end_date
            if is_leave_date_taken(start_date, end_date):
                messages.error(request, "The selected leave dates overlap with an existing leave request.")
                return render(request, 'employee_leave/request_leave.html', {'form': form})

            leave_request.save()
            if leave_request.manager:
                subject = f"New Leave Request from {request.user.get_full_name()}"
                message = f"Dear {leave_request.manager.get_full_name() if leave_request.manager else 'Manager'},\n\nYou have a new leave request from {request.user.get_full_name()}.\n\nLeave Type: {leave_request.leave_type}\nStart Date: {leave_request.start_date}\nEnd Date: {leave_request.end_date}\n\nPlease review and approve/reject the request."
                from_email = leave_request.employee.email 
                recipient_list = [leave_request.manager.email]  
                send_mail(subject, message, from_email, recipient_list)

            messages.success(request, "Your leave request has been successfully submitted and is awaiting approval from your manager.")
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
    manager_approved_leaves = employee_leaves.filter(status='manager_approved')
    rejected_leaves_by_manager = employee_leaves.filter(status='rejected')
    approved_by_hr_leaves = employee_leaves.filter(status='approved_by_hr')
    rejected_by_hr_leaves = employee_leaves.filter(status='rejected_by_hr')

    total_leave_taken = sum((leave.end_date - leave.start_date).days + 1 for leave in approved_by_hr_leaves)

    leave_status = "You have remaining leave days."
    remaining_leave = 30 - total_leave_taken  
    if total_leave_taken >= 30:
        leave_status = "You have exhausted all your leave days."

    total_leave_taken = max(total_leave_taken, 0)
    remaining_leave = max(remaining_leave, 0)
    
    fig, ax = plt.subplots(figsize=(6, 6)) 
    ax.pie([total_leave_taken, remaining_leave], 
           labels=['Leave Taken', 'Remaining Leave'], 
           autopct='%1.0f%%',
           colors=['#ff6347', '#32cd32'],    
           startangle=90, 
           pctdistance=0.85,
           explode=(0.1, 0))   

    ax.axis('equal') 
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    leave_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    context = {
        'employee_name': request.user.get_full_name(),
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'rejected_leaves': rejected_leaves,
        'manager_approved_leaves': manager_approved_leaves,
        'rejected_leaves_by_manager':rejected_leaves_by_manager,
        'approved_by_hr_leaves': approved_by_hr_leaves,
        'rejected_by_hr_leaves': rejected_by_hr_leaves,
        'total_leave_taken': total_leave_taken,
        'leave_status': leave_status,
        'leave_chart': leave_chart,  
    }

    return render(request, 'employee_leave/leave_requests.html', context)