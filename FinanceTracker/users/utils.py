from django.core.mail import send_mail
from .models import User

def notify_users():
    users = User.objects.filter(notified_reset=False)
    for user in users:
        send_mail(
            'Monthly Expense Reset',
            'Your expenses have been reset for the month.',
            'admin@yourdomain.com',
            [user.email],
        )
        user.notified_reset = True
        user.save()
