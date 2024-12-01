from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib import messages
from .models import DonationRequest , Donation
from django.http import HttpResponseBadRequest

# Create your views here.

def add_donation_request(request):
    if request.method == 'POST':
        if not hasattr(request.user, 'shelter'):
            return HttpResponseBadRequest("You do not have shelter permissions.")
        
        shelter = request.user.shelter  
        donation_type = request.POST.get('donation_type')
        amount_requested = request.POST.get('amount_requested')
        description = request.POST.get('description')

        if donation_type in ['food', 'supplies'] and not amount_requested:
            amount_requested = None
        else:
            try:
                amount_requested = float(amount_requested)
            except ValueError:
                messages.error(request, 'Invalid amount requested.')
                return redirect('donations:add_donation_request')

        donation_request = DonationRequest(
            shelter=shelter,
            donation_type=donation_type,
            amount_requested=amount_requested,
            description=description,
        )
        donation_request.save()

        messages.success(request, 'Your donation request has been successfully submitted!')
        return redirect('donations:donation_request_list')

    return render(request, 'donations/add_donation_request.html')

def donation_request_list(request):
    donation_type = request.GET.get('donation_type', '')
    fulfilled_status = request.GET.get('fulfilled_status', '')

    filters = {}
    if donation_type:
        filters['donation_type__icontains'] = donation_type
    if fulfilled_status:
        filters['fulfilled'] = fulfilled_status.lower() == 'true'

    donation_requests = DonationRequest.objects.filter(**filters)

    return render(request, 'donations/donation_request_list.html', {'donation_requests': donation_requests})


def edit_donation_request(request, request_id):
    donation_request = get_object_or_404(DonationRequest, id=request_id)

    if request.user != donation_request.shelter.user:
        messages.error(request, "You are not authorized to edit this request.")
        return redirect('donations:donation_request_list')  

    if request.method == 'POST':
        donation_type = request.POST.get('donation_type')
        amount_requested = request.POST.get('amount_requested')
        description = request.POST.get('description')
        fulfilled = 'fulfilled' in request.POST 

        if donation_type in ['food', 'supplies'] and not amount_requested:
            amount_requested = None
        else:
            try:
                amount_requested = float(amount_requested)
            except ValueError:
                amount_requested = None

        donation_request.donation_type = donation_type
        donation_request.amount_requested = amount_requested
        donation_request.description = description
        donation_request.fulfilled = fulfilled  

        donation_request.save()

        messages.success(request, "Donation request updated successfully.")
        return redirect('donations:donation_request_list')  

    return render(request, 'donations/edit_donation_request.html', {'donation_request': donation_request})


def delete_donation_request(request, donation_id):
    donation_request = get_object_or_404(DonationRequest, id=donation_id)

    if request.user != donation_request.shelter.user:
        messages.error(request, "You are not authorized to delete this request.")
        return redirect('donations:donation_request_list')

    donation_request.delete()
    messages.success(request, "Donation request has been successfully deleted.")
    return redirect('donations:donation_request_list')

def make_donation(request, donation_request_id):
    donation_request = get_object_or_404(DonationRequest, id=donation_request_id)

    if request.method == 'POST':
        donor_name = request.POST.get('donor_name', '')
        donation_type = request.POST.get('donation_type', '')
        amount = request.POST.get('amount', '')
        shipping_company = request.POST.get('shipping_company', '')
        tracking_number = request.POST.get('tracking_number', '')
        payment_method = request.POST.get('payment_method', None)

        if donation_type == 'cash' and amount and payment_method:

            donation = Donation(
                donor_name=donor_name,
                donation_type=donation_type,
                amount=amount,
                payment_method=payment_method,
                donation_request=donation_request
            )
            donation.save()
            messages.success(request, f"Thank you for your monetary donation via {payment_method}!")
            return redirect('donations:donation_request_list')

        elif donation_type == 'supplies' and shipping_company and tracking_number:

            donation = Donation(
                donor_name=donor_name,
                donation_type=donation_type,
                shipping_company=shipping_company,
                tracking_number=tracking_number,
                donation_request=donation_request
            )
            donation.save()
            messages.success(request, "Thank you for your supplies donation!")
            return redirect('donations:donation_request_list')

        else:
            messages.error(request, "Please fill all required fields.")
            return redirect('donations:make_donation', donation_request_id=donation_request.id)

    return render(request, 'donations/donate.html', {'donation_request': donation_request})
