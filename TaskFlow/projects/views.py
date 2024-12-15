from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from django.http import HttpRequest
from django.contrib.auth.models import User
from .forms import ProjectForm
from .utils import send_invitation_email

@login_required
def project_list(request: HttpRequest):
    # Filter projects where the logged-in user is the manager
    projects = Project.objects.filter(manager=request.user)
    return render(request, "projects/project_list.html", {"projects": projects})

@login_required
def project_detail(request: HttpRequest, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "projects/project_detail.html", {"project": project})



from django.contrib.auth.models import User
from .utils import send_invitation_email

def project_create(request):
    if request.method == 'POST':
        # Capture project and team member details from the form
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Create the project instance
        project = Project.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            manager=request.user  # Assign the logged-in user as the manager
        )

        # Process team members
        member_names = request.POST.getlist('member_name[]')
        member_roles = request.POST.getlist('member_role[]')
        member_emails = request.POST.getlist('member_email[]')

        # Collect user objects for the team members
        member_objects = []
        for name, role, email in zip(member_names, member_roles, member_emails):
            # Create a User instance or retrieve an existing one
            user, created = User.objects.get_or_create(email=email, defaults={
                'username': email.split('@')[0],  # Use email prefix as username
            })
            member_objects.append(user)

        # Assign members to the project
        project.members.set(member_objects)

        # Save the project with updated members
        project.save()

        # Show success message and redirect to dashboard
        messages.success(request, "Project created successfully!")
        return redirect('Users:dashboard_view', username=request.user.username)

    # Render the project creation form
    return render(request, 'projects/project_create.html')

@login_required
def project_update(request, pk):
    # Ensure only the manager can edit the project
    project = get_object_or_404(Project, pk=pk, manager=request.user)
    
    if request.method == "POST":
        project.name = request.POST["name"]
        project.description = request.POST["description"]
        project.start_date = request.POST["start_date"]
        project.end_date = request.POST["end_date"]
        members = request.POST.getlist("members")
        project.members.set(members)  # Update members
        project.save()
        messages.success(request, "Project updated successfully.")
        return redirect("projects:project_detail", pk=project.pk)
    
    user_list = User.objects.exclude(id=request.user.id)
    return render(request, "projects/project_update.html", {"project": project, "user_list": user_list})

@login_required
def project_delete(request: HttpRequest, pk):
    # Ensure only the manager can delete the project
    project = get_object_or_404(Project, pk=pk, manager=request.user)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect("projects:project_list")

    return render(request, "projects/project_delete.html", {"project": project})