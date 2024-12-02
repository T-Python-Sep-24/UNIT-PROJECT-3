from django.shortcuts import render ,redirect, get_object_or_404
from .models import AdoptionRequest
from pets.models import Pet
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required
def request_adoption(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    
    existing_request = AdoptionRequest.objects.filter(pet=pet, user=request.user).first()
    if existing_request:
        messages.warning(request, 'You have already sent an adoption request for this pet.')
        return render(request, 'adoptions/already_requested.html', {'pet': pet})
    
    if request.method == 'POST':
        comment = request.POST.get('comments', '')  

        adoption_request = AdoptionRequest.objects.create(
            pet=pet,
            user=request.user,
            status='pending',
            comments=comment  
        )
        messages.success(request, 'Your adoption request has been sent successfully!')
        return redirect('pets:pet_detail', pet_id=pet.id)

    return render(request, 'adoptions/request_adoption.html', {'pet': pet})



def handle_adoption_request(request, request_id, action):
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)

    pet = adoption_request.pet

    if not (pet.user == request.user or pet.shelter == request.user):
        messages.error(request, "You are not authorized to take this action.")
        return redirect('pets:pet_detail', pet_id=pet.id)

    if adoption_request.status == 'pending':
        comment = request.POST.get('comments', '')  
        if action == 'accept':
            adoption_request.status = 'accepted'
            if not comment:
                comment = "Congratulations! Your adoption request has been accepted, and you will be contacted shortly."
            adoption_request.comment_by_approver = comment 
            adoption_request.save()

            messages.success(request, f"The adoption request for {adoption_request.pet.name} has been accepted successfully! {comment}")

        elif action == 'reject':
            adoption_request.status = 'rejected'
            if not comment:
                comment = "We regret to inform you that your adoption request has not been accepted. We wish you all the best in your future endeavors."
            adoption_request.comment_by_approver = comment 
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

