from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from django.http import HttpRequest
from django.contrib.auth.models import User
from .forms import ProjectForm

@login_required
def project_list(request: HttpRequest):
    projects = Project.objects.filter(created_by=request.user)
    return render(request, "projects/project_list.html", {"projects": projects})

@login_required
def project_detail(request: HttpRequest, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "projects/project_detail.html", {"project": project})

@login_required
def project_create(request):
    user_roles = request.user.roles.filter(name="Manager")
    if not user_roles.exists():
        messages.error(request, "You do not have permission to add a project.")
        return redirect('Users:dashboard_view')

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = user_roles.first()  # Assign the logged-in manager role
            project.save()
            form.save_m2m()  # Save the many-to-many relationships
            messages.success(request, "Project added successfully!")
            return redirect('Users:dashboard_view')
    else:
        form = ProjectForm()

    return render(request, "projects/add_project.html", {"form": form})

@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk, created_by=request.user)  # Ensure only the manager can edit
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
    project = get_object_or_404(Project, pk=pk, created_by=request.user)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect("projects:project_list")

    return render(request, "projects/project_delete.html", {"project": project})
