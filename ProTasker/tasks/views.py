from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from .models import Task,Project,Notification
from .forms import TaskForm
from django.contrib import messages
from django.shortcuts import get_object_or_404



# Create your views here.
def task_view(request: HttpRequest):
    priority_filter = request.GET.get('priority', None)

    if priority_filter:
        tasks = Task.objects.filter(assignee=request.user, priority=priority_filter)
    else:
        tasks = Task.objects.filter(assignee=request.user)

    return render(request, 'main/task.html', {'tasks': tasks, 'priority_filter': priority_filter})

def create_task(request: HttpRequest):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            # حفظ المهمة
            task = form.save()

            # إضافة إشعار للمستخدم الذي تم تعيين المهمة له
            Notification.objects.create(
                user=task.assignee,
                message=f"New task '{task.title}' has been assigned to you."
            )

            # عرض رسالة نجاح وإعادة التوجيه
            messages.success(request, "Task created successfully!", "alert-success")
            return redirect('tasks:task_view')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = TaskForm()

    users = User.objects.all()
    projects = Project.objects.all()

    return render(request, 'main/create_task.html', {
        'form': form,
        'users': users,
        'projects': projects,
    })



def update_task(request: HttpRequest, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance=task)

        if task_form.is_valid(): 
            task_form.save()
            messages.success(request, "Task updated successfully!", "alert-success")
            return redirect("tasks:task_view")
    else:
        task_form = TaskForm(instance=task) 
    users = User.objects.all()
    projects = Project.objects.all()

    return render(request, 'main/update_task.html', {'task_form': task_form,'task': task,'users': users,'projects': projects,})


def task_delete_view(request:HttpRequest, task_id:int):

    try:
        task = Task.objects.get(pk=task_id)
        task.delete()
        messages.success(request, "Deleted task successfully", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't Delete game", "alert-danger")


    return redirect("tasks:task_view")
