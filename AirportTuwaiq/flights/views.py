from django.shortcuts import render ,redirect 
from django.http import HttpRequest , HttpResponse
from django.core.paginator import Paginator
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
    

def flight_list_view(request:HttpRequest):

    query = request.GET.get('search', '').strip()
    
    # Fetch flights based on the query
    if query:
        flights = Flight.objects.filter(flight_number__icontains=query)
        if not flights.exists():
            messages.error(request, f"No flights found for flight number '{query}'.", "alert-danger")
    else:
        flights = Flight.objects.all()
    paginator = Paginator(flights, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    return render(request, 'flights/flight_list.html', {'page_obj': page_obj})



def flight_detail_view(request: HttpRequest, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)  # Fetch flight using objects.get
    except Flight.DoesNotExist:
            return redirect('flights:flight_list_view')  # Redirect if the flight doesn't exist

    return render(request, 'flights/flight_detail.html', {'flight': flight})



def edit_flight_view(request: HttpRequest, flight_id): 
    try:
        flight = Flight.objects.get(pk=flight_id)  
        if request.method == "POST":
            from_city = City.objects.get(name=request.POST["from_city"])
            to_city = City.objects.get(name=request.POST["to_city"])
            if from_city == to_city:
                messages.error(request, "Origin and destination cities must be different.", "alert-danger")
                return redirect('flights:edit_flight', flight_id=flight.id)
            
            flight.flight_number = request.POST["flight_number"]
            flight.from_city = from_city
            flight.to_city  = to_city
            flight.departure_time = request.POST["departure_time"]
            flight.arrival_time = request.POST["arrival_time"]
            flight.price = request.POST["price"]
            flight.available_seats = request.POST["available_seats"]
            flight.save()  
            print("is done update data")
            messages.success(request, f"Flight {flight.flight_number} updated successfully!", "alert-success")
            return redirect('flights:flight_detail_view', flight_id=flight.id) 
    except Flight.DoesNotExist:
        messages.error(request, "Flight not found.", "alert-danger")
        return redirect('flights:flight_list_view') 
    except Exception as e :
        print( "this is Catching:", e)
    
    return render(request, 'flights/edit_flight.html', {'flight': flight})