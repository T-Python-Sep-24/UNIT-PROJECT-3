from django.shortcuts import render ,redirect 
from django.http import HttpRequest , HttpResponse
from django.contrib import messages
from .models import City, Flight

# Create your views here.
def add_flight_view(request:HttpRequest): 
    try :
        if request.method == "POST": 
            from_city=City.objects.get(name=request.POST["from_city"])
            to_city=City.objects.get(name=request.POST["to_city"])
            
            if from_city == to_city : 
                messages.error(request, "Origin and destination cities must be different.", "alert-danger")
                return redirect('flights:add_flight_view')
            new_flight = Flight(flight_number=request.POST["flight_number"],
                                from_city=from_city,
                                to_city=to_city, 
                                departure_time=request.POST["departure_time"],
                                arrival_time= request.POST["arrival_time"],
                                price= request.POST["price"],
                                available_seats= request.POST["available_seats"]  )
            messages.success(request, f"Flight {new_flight.flight_number} added successfully!" , "alert-success")
            new_flight.save()
            #test!
            print("is done saved data ")       
            return redirect('flights:add_flight_view')
    except Exception as e:
        print(e)
    return render(request, 'flights/add_flight.html')
    