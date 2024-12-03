from django.shortcuts import render , redirect
from .models import Director
from django.http import HttpRequest,HttpResponse
from django.contrib import messages
from .forms import DirectorForm
# Create your views here.


def all_directors_view(request:HttpRequest):
    directors=Director.objects.all()

    return render(request,'directors/all_directors.html',context={'directors':directors})

def director_detail_view(request:HttpRequest,director_id : int):
    director = Director.objects.get(pk=director_id)
    movies = director.movie_set.all()
    return render(request, 'directors/director_detail.html', {'director': director,'movies':movies})

def add_director_view(request:HttpRequest):
    if not (request.user.is_staff and request.user.has_perm('directors.add_director')):
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect ("directors:all_directors_view")
    
    if request.method == 'POST':
        director_form = DirectorForm(request.POST)
        if director_form.is_valid():
            director_form.save()
            messages.success(request, "added director Successfuly", "alert-success")
            return redirect('directors:all_directors_view')
        else:
            messages.error(request,director_form.errors,'alert-danger')  
  
    return render(request, 'directors/add_director.html')

def director_update_view(request:HttpRequest,director_id:int):
    if not (request.user.is_staff and request.user.has_perm('directors.change_director')):
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect ("directors:all_directors_view")
    
    director=Director.objects.get(pk=director_id)
    if not request.user.is_staff:
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect('directors:director_detail_view',director_id=director.id)
    
    if request.method == 'POST':
        director_form=DirectorForm(instance=director,data=request.POST)
        if director_form.is_valid():
            director_form.save()
            messages.success(request,' director updated successfully','alert-success')
            return redirect('directors:director_detail_view',director_id=director.id)
        else:
            messages.error(request,director_form.errors,'alert-danger')

    return render(request,'directors/update_director.html',context={'director':director})

def delete_director_view(request:HttpRequest, director_id:int):
    if not (request.user.is_staff and request.user.has_perm('directors.delete_director')):
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect ("directors:all_directors_view")
    
    director=Director.objects.get(pk=director_id)
    if not request.user.is_staff:
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect('directors:director_detail_view',director_id=director.id)
    try:
            director.delete()
            messages.success(request, f"Deleted {director.name} successfully", "alert-success")
            return redirect ("directors:all_directors_view")
    except Exception as e:
            print(e)
            messages.error(request, f"Couldn't Delete {director.name} ", "alert-danger")
            return redirect ("directors:all_directors_view")
   
