from django.shortcuts import render ,redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Pet
from django.core.paginator import Paginator
from .forms import PetForm
from adoptions.models import AdoptionRequest


# Create your views here.

@login_required 
def add_pet(request):
    if request.method == 'POST':
      
        name = request.POST.get('name')
        image = request.FILES.get('image')
        species = request.POST.get('species')
        breed = request.POST.get('breed')
        age = request.POST.get('age')
        health_status = request.POST.get('health_status')
        adoption_status = request.POST.get('adoption_status')
        medical_history = request.POST.get('medical_history')
        location = request.POST.get('location')

      
        if not name or not species or not age or not health_status or not adoption_status:
            return HttpResponse("All required fields must be filled!", status=400)

      
        pet = Pet(
            name=name,
            image=image,
            species=species,
            breed=breed,
            age=age,
            health_status=health_status,
            adoption_status=adoption_status,
            medical_history=medical_history,
            location=location,
            user=request.user 
        )
        pet.save()

        return redirect('pets:pet_list_view')  

    return render(request, 'pets/add_pet.html')


def pet_list_view(request):
    search_query = request.GET.get('search', '')
    adoption_status = request.GET.get('adoption_status', '')

    pets = Pet.objects.all().order_by('-created_at')  

    if search_query:
        pets = pets.filter(name__icontains=search_query)

    if adoption_status:
        pets = pets.filter(adoption_status=adoption_status)

    
    paginator = Paginator(pets, 8)  
    page_number = request.GET.get('page') 
    pets_page = paginator.get_page(page_number) 

    return render(request, 'pets/pet_list.html', {'pets': pets_page})

def pet_detail_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    
    if request.user.is_authenticated:
        already_requested = AdoptionRequest.objects.filter(pet=pet, user=request.user).exists()
    else:
        already_requested = False  

    return render(request, 'pets/pet_detail.html', {'pet': pet, 'already_requested': already_requested})

def edit_pet(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
    except Pet.DoesNotExist:
       
        return redirect('pets:edit_pet')  

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pets:pet_detail', pet_id=pet.id)
    else:
        form = PetForm(instance=pet)
    
    return render(request, 'pets/edit_pet.html', {'form': form, 'pet': pet})

def delete_pet(request, pet_id):
    pet = Pet.objects.filter(id=pet_id).first()

    if pet:  
        if request.user == pet.user: 
            pet.delete() 
            return redirect('pets:pet_list_view') 
        else:
            return redirect('pets:pet_detail', pet.id) 
    else:
        return redirect('pets:pet_list_view')