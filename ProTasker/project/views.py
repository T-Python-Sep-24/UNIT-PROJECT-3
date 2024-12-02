from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest,HttpResponse
from .models import Project
from .forms import ProjectForm, TeamMemberForm
from .models import Project, TeamMember,ProjectFile
from django.contrib.auth.models import User
from tasks.models import Task
from django.contrib import messages


from project.models import TeamMember
# Create your views here.


def project_view(request:HttpRequest):
     projects = Project.objects.all()  
     return render(request, 'main/project.html', {'projects': projects})

        
   




def dashboard_view(request:HttpRequest):
    return render(request,"main/dashboard.html")






def create_project_view(request:HttpRequest):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        team_formset = TeamMemberForm.TeamMemberFormSet(request.POST)

        if project_form.is_valid() and team_formset.is_valid():
            project = project_form.save()
            
            for form in team_formset:
                if form.cleaned_data.get('user') and form.cleaned_data.get('role'):
                    form.instance.project = project
                    form.save()

                    user = form.cleaned_data.get('user')
                    role = form.cleaned_data.get('role')
                    if role == 'Leader':
                        user.is_staff = True 
                        user.save()
                    else:
                        user.is_staff = False  
                        user.save()

            return redirect('project:project_view')

    else:
        project_form = ProjectForm()
        team_formset = TeamMemberForm.TeamMemberFormSet(queryset=TeamMember.objects.none()) 

    return render(request, 'main/create_project.html', {
        'project_form': project_form,
        'team_formset': team_formset,
    })




def upload_file(request:HttpRequest, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        title = request.POST['title']
        file = request.FILES['file']
        ProjectFile.objects.create(project=project, title=title, file=file)
        return redirect('project:project_detail_view', project_id=project.id)

    return render(request, "main/project_detail.html", {'project': project})

def project_detail_view(request:HttpRequest,project_id):
    project = get_object_or_404(Project, pk=project_id)
    tasks = Task.objects.filter(project=project).prefetch_related('comment_set')
    
  
    tasks = Task.objects.filter(project=project)
    
   
    return render(request, 'main/project_detail.html', {'project': project, 'tasks': tasks})








def update_project_view(request: HttpRequest, project_id):
 
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        
        if project_form.is_valid():
            project_form.save()
            messages.success(request, "Update Project Successfully", "alert-success")
            return redirect("project:project_detail_view", project_id=project.id)
           
    else:
    
        project_form = ProjectForm(instance=project)

  
    return render(request, 'main/update_project.html', { 'project_form': project_form, 'project': project, })



def project_delete_view(request:HttpRequest, project_id:int):

    try:
        project = Project.objects.get(pk=project_id)
        project.delete()
        messages.success(request, "Deleted Project successfully", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't Delete project", "alert-danger")


    return redirect("project:project_view")


