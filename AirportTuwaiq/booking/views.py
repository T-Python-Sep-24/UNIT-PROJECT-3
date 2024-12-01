from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from flights.models import Flight
from .models import Booking
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout

def search_flights_view(request: HttpRequest):
    flights = Flight.objects.none()  # Start with an empty queryset
    error_message = None

    # Search by cities and date
    from_city = request.GET.get('from_city')
    to_city = request.GET.get('to_city')
    date = request.GET.get('date')

    if from_city or to_city or date:
        flights = Flight.objects.all()  # Populate the queryset only if search criteria are provided
        flights = flights.filter(
            from_city__name__icontains=from_city if from_city else "",
            to_city__name__icontains=to_city if to_city else "",
            departure_time__date=date if date else None
        )
        if not flights.exists():
            error_message = "No flights match the given criteria."
    else:
        error_message = "Please provide search criteria."

    # Apply filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    departure_time = request.GET.get('departure_time')

    if min_price:
        flights = flights.filter(price__gte=min_price)
    if max_price:
        flights = flights.filter(price__lte=max_price)
    if departure_time:
        flights = flights.filter(departure_time__gte=departure_time)

    return render(request, 'booking/search_flights.html', {'flights': flights, 'error_message': error_message})


def booking_detail_view(request: HttpRequest, flight_id):
    try:
        # Fetch the flight using the flight ID
        flight = Flight.objects.get(pk=flight_id)
        return render(request, 'booking/booking_detail.html', {'flight': flight})
    except Flight.DoesNotExist:
        messages.error(request, "Flight not found.", "alert-danger")
        return redirect('booking:search_flights')

    # Render the booking details template
    # return render(request, 'booking/booking_detail.html', {'flight': flight})

def filter_flights_view(request):
    flights = Flight.objects.all()

    # Apply price filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        flights = flights.filter(price__gte=min_price)
    if max_price:
        flights = flights.filter(price__lte=max_price)

    # Apply departure time filter
    departure_time = request.GET.get('departure_time')
    if departure_time:
        flights = flights.filter(departure_time__gte=departure_time)

    return render(request, 'booking/search_flights.html', {'flights': flights})


  
def confirm_booking_view(request: HttpRequest, flight_id):

    flight = Flight.objects.get(pk=flight_id)
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to confirm a booking.", "alert-danger")
        return redirect("users:sign_in_view")
    if request.method == "POST":    
        booking = Booking(
            flight=flight,
            customer=request.user, 
            seats=1,  
            status="CONFIRMED",
            total_price=flight.price
        )
        booking.save()
        messages.success(request, f"Booking successfully confirmed for flight {flight.flight_number}. Welcome {request.user.first_name}!", "alert-success")
        return redirect('booking:search_flights', flight_id=flight.id)

    return render(request, 'booking/confirm_booking.html', {'flight': flight ,'customer': request.user})