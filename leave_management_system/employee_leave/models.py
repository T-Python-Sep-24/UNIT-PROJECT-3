from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class LeaveRequest(models.Model):
    LEAVE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('manager_approved', 'Manager Approved'),
        ('rejected', 'Rejected by Manager'),
        ('approved_by_hr', 'Approved by HR'),
        ('rejected_by_hr', 'Rejected by HR'),
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

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_leave_requests_employee')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='employee_manager_leave_requests', on_delete=models.CASCADE, default=1)
    hr = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='employee_manager_hr_leave_requests', on_delete=models.CASCADE, default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=100, choices=LEAVE_TYPE_CHOICES)
    status = models.CharField(max_length=16, choices=LEAVE_STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, null=True)
    manager_reason = models.TextField(blank=True, null=True)
    hr_reason = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to='leave_documents/', null=True, blank=True)
    sent_to_hr = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    days = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.leave_type} leave from {self.start_date} to {self.end_date}"
    
    def save(self, *args, **kwargs):
        if not self.manager and self.employee.profile.manager:
            self.manager = self.employee.profile.manager
        
        if not self.days:
            self.days = (self.end_date - self.start_date).days + 1
        
        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, related_name='manages', on_delete=models.SET_NULL, null=True, blank=True)
    hr = models.ForeignKey(User, related_name='hr_assigned', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
