from django.db import models
from django.contrib.auth.models import User

class LeaveRequest(models.Model):
    LEAVE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    LEAVE_TYPE_CHOICES = [
        ('sick', 'Sick Leave'),
        ('annual', 'Annual Leave'),
        ('maternity', 'Maternity Leave'),
        ('emergency', 'Emergency Leave'),
        ('study', 'Study Leave'),
        ('compassionate', 'Compassionate Leave'),
        ('unpaid', 'Unpaid Leave'),
        ('public_holiday', 'Public Holiday'),
        ('personal', 'Personal Leave'),
        ('other', 'Other'),
    ]
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager_leave_requests')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_leave_requests_manager') 
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=100, choices=LEAVE_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=LEAVE_STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, null=True)
    manager_reason = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to='leave_documents/', null=True, blank=True)
    sent_to_hr = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.leave_type} leave from {self.start_date} to {self.end_date}"
