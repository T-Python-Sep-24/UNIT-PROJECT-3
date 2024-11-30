from django.shortcuts import render ,redirect, get_object_or_404
from .models import AdoptionRequest
from pets.models import Pet
from django.contrib import messages



# Create your views here.


def request_adoption(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    
    existing_request = AdoptionRequest.objects.filter(pet=pet, user=request.user).first()
    if existing_request:
        messages.warning(request, 'You have already sent an adoption request for this pet.')
        return render(request, 'adoptions/already_requested.html', {'pet': pet})
    
    if request.method == 'POST':
        adoption_request = AdoptionRequest.objects.create(pet=pet, user=request.user, status='pending')
        messages.success(request, 'Your adoption request has been sent successfully!')
        return redirect('pets:pet_detail', pet_id=pet.id)
    
    return render(request, 'adoptions/request_adoption.html', {'pet': pet})



def handle_adoption_request(request, request_id, action):
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)

    if adoption_request.status == 'pending':
        if action == 'accept':
            adoption_request.status = 'accepted'
            adoption_request.save()
            messages.success(request, f"The adoption request for {adoption_request.pet.name} has been accepted successfully!")

        elif action == 'reject':
            adoption_request.status = 'rejected'
            adoption_request.save()
            messages.info(request, f"The adoption request for {adoption_request.pet.name} has been rejected.")
        elif action == 'cancel' and adoption_request.user == request.user:
            adoption_request.delete()
            messages.info(request, "The adoption request has been successfully canceled.")
    
    if hasattr(request.user, 'individual_user'):
        return redirect('accounts:individual_profile', individual_id=request.user.individual_user.id)
    elif hasattr(request.user, 'shelter'):
        return redirect('accounts:shelter_profile', shelter_id=request.user.shelter.id)
    else:
        messages.error(request, "An error occurred while processing the request.")
        return redirect('accounts:login')

