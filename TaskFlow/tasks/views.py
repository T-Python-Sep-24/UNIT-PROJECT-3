from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task,Project
from .forms import TaskForm , CommentForm
from django.contrib.auth.models import User

@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect("tasks:task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/create_task.html", {"form": form})

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = task.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.created_by = request.user
            comment.save()
            return redirect('tasks:task_detail', task_id=task.id)
    else:
        form = CommentForm()

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'comments': comments,
        'form': form,
    })


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.title = request.POST["title"]
        task.description = request.POST["description"]
        task.status = request.POST["status"]
        task.priority = request.POST["priority"]
        task.due_date = request.POST["due_date"]
        task.assigned_to_id = request.POST["assigned_to"]
        task.project_id = request.POST["project"]
        task.save()

        messages.success(request, "Task updated successfully.", "alert-success")
        return redirect("tasks:task_detail", task_id=task.id)

    users = User.objects.all()
    projects = Project.objects.all()
    return render(request, "tasks/update_task.html", {"task": task, "users": users, "projects": projects})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect("tasks:task_list")
    return render(request, "tasks/delete_task.html", {"task": task})
