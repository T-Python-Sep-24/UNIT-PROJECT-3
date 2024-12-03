from django.shortcuts import render , redirect
from django.http import HttpRequest,HttpResponse
from django.db import transaction
from django.core.paginator import Paginator
from .models import Screening , Ticket
from .forms import ScreeningForm
from movies.models import Movie
from django.urls import reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.html import strip_tags
import json

def all_screens_view(request :HttpRequest):
    if not (request.user.is_staff and request.user.has_perm("screens.view_screening")):
        messages.warning(request,'You do not have permission','alert-warning')
        return redirect('main:home_view')
    
    movies=Movie.objects.all()
    selected_movie = request.GET.get('movie', None)

    screenings = Screening.objects.all().order_by('showtime')
    if selected_movie:
        screenings = screenings.filter(movie__id=selected_movie)
    
    paginator = Paginator(screenings, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'screens/all_screens.html', context = {'screenings': page_obj,'movies':movies,'selected_movie':selected_movie})


def add_screen_view(request:HttpRequest):
    if not (request.user.is_staff and request.user.has_perm("screens.add_screening")):
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
    if not (request.user.is_staff and request.user.has_perm("screens.change_screening")):
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
    if not (request.user.is_staff and request.user.has_perm("screens.delete_screening")):
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
    


def booking_view(request:HttpRequest, screen_id:int):
    if not request.user.is_authenticated:
        messages.warning(request, 'Login First to access booking', 'alert-warning')
        return redirect(f'{reverse("accounts:signin_view")}?next={request.path}')
    screening = Screening.objects.get(pk=screen_id)
    seats = screening.get_seats()  
    total_price = screening.price
    user_budget = request.user.profile.budget
    rows = {row: {f"{row}{num}": seats.get(f"{row}{num}", False) for num in "123456"} for row in "ABCD"}
    
    
    if request.method == "POST":
        
        selected_seats = request.POST.get("selected_seats", "")
        
        selected_seats = selected_seats.split(",") if selected_seats else []
        total_price= len(selected_seats)* total_price
        
        if total_price > user_budget:
            messages.error(request, "Insufficient budget to complete this booking.", 'alert-danger')
            return redirect('screens:booking_view',screen_id=screen_id)
        
        try:
           
            with transaction.atomic():
                
                profile = request.user.profile
                profile.budget -= total_price
                profile.save()
                for seat in selected_seats:
                    if not seats.get(seat, False):
                        
                        raise ValueError(f"Seat {seat} is already booked.")
                    seats[seat] = False
                
                screening.seats = json.dumps(seats)
                screening.save()

                ticket=Ticket(user=request.user,screening=screening,seat_numbers=selected_seats,total_price=total_price)
                ticket.save()

            #email
            # email_template = render_to_string('bookings/email/booking_confirmation.html', {
            #         'user': request.user,
            #         'ticket': ticket,
            #         'screening': screening,
            #         'selected_seats': selected_seats,
            #         'poster_url': screening.movie.poster.url,  
            #     })
            # send_to = request.user.email
            # email_message = EmailMessage("confiramation", email_template, settings.EMAIL_HOST_USER, [send_to])
            # email_message.content_subtype = "html"
            # email_message.send()

            messages.success(request, "Your booking was successful!", 'alert-success')
            return redirect('accounts:profile_view', user_name=request.user.username)

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}", 'alert-danger')
            print(e)
            return redirect('main:home_view')

    return render(request, 'bookings/booking.html', {'screening': screening, 'rows': rows, 'total_price': total_price})

    
