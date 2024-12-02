from django.shortcuts import render , redirect
from django.http import HttpRequest,HttpResponse
from django.core.paginator import Paginator
from .models import Screening
from .forms import ScreeningForm
from movies.models import Movie
from django.contrib import messages

def all_screens_view(request :HttpRequest):
    if not request.user.is_staff:
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect('main:home_view')
    
    movies=Movie.objects.all()
    selected_movie = request.GET.get('movie', None)

    screenings = Screening.objects.all().order_by('showtime')
    if selected_movie:
        screenings = screenings.filter(movie__id=selected_movie)
    
    paginator = Paginator(screenings, 10)  # 10 screenings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'screens/all_screens.html', context = {'screenings': page_obj,'movies':movies,'selected_movie':selected_movie})


def add_screen_view(request:HttpRequest):
    if not request.user.is_staff:
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect('main:home_view')
    screen_form=ScreeningForm()
    movies = Movie.objects.all()
    if request.method == 'POST':
        try:
            screen_form=ScreeningForm(request.POST)
            if screen_form.is_valid():
                screen_form.save()
                messages.success(request, "Booked Screen Successfuly", "alert-success")
                return redirect('screens:all_screens_view')
            else:
                messages.error(request,screen_form.errors,'alert-danger')
        except Exception as e:
            print(e)
            messages.error(request,"something went wrong",'alert-danger')
            return redirect('main:home_view') 
       
    return render(request, 'screens/add_screen.html', {'movies': movies})

def update_screen_view(request: HttpRequest, screen_id: int):
    if not request.user.is_staff:
        messages.warning(request, 'You do not have permission', 'alert-warning')
        return redirect('main:home_view')

    
    screening = Screening.objects.get(pk=screen_id)
    movies=Movie.objects.all()

    if request.method == 'POST':
        form = ScreeningForm(request.POST, instance=screening)
        if form.is_valid():
            form.save()
            messages.success(request, 'Screening updated successfully', 'alert-success')
            return redirect('screens:all_screens_view')
        else:
            messages.error(request, form.errors, 'alert-danger')

    return render(request, 'screens/update_screen.html', {'screening': screening,'movies':movies})

def delete_screen_view(request:HttpRequest , screen_id: int):
    if not request.user.is_staff:
        messages.warning(request, 'You do not have permission', 'alert-warning')
        return redirect('main:home_view')
    
    screening = Screening.objects.get(pk=screen_id)
    try:
            screening.delete()
            messages.success(request, f"Deleted {screening.movie.title} in {screening.theater} successfully", "alert-success")
            return redirect('screens:all_screens_view')
    except Exception as e:
            print(e)
            messages.error(request, f"Couldn't Delete {screening.movie.title} in {screening.theater} ", "alert-danger")
            return redirect('screens:all_screens_view')
    
