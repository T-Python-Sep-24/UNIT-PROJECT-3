from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_invitation_email(email, project_name, inviter_name):
    subject = f"You've been invited to join the project: {project_name}"
    message = render_to_string('emails/invitation_email.html', {
        'project_name': project_name,
        'inviter_name': inviter_name,
    })
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
