from django.shortcuts import render , redirect , get_object_or_404
from django.contrib import messages
from .models import DonationRequest , Donation
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator



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
    filters = {}

    donation_type = request.GET.get('donation_type', '')
    if donation_type:
        filters['donation_type__icontains'] = donation_type

    fulfilled_status = request.GET.get('fulfilled_status', '')
    if fulfilled_status:
        filters['fulfilled'] = fulfilled_status.lower() == 'true'

    donation_requests = DonationRequest.objects.filter(**filters).annotate(
        total_donated=Sum('donations__amount')
    )

    for req in donation_requests:
        if req.amount_requested and req.total_donated:
            req.remaining = req.amount_requested - req.total_donated
        else:
            req.remaining = req.amount_requested if req.amount_requested else 0

    
    paginator = Paginator(donation_requests, 8) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)  

    return render(request, 'donations/donation_request_list.html', {'donation_requests': page_obj})


def edit_donation_request(request, request_id):
    donation_request = get_object_or_404(DonationRequest, id=request_id)

    if not hasattr(request.user, 'shelter') or request.user != donation_request.shelter.user:
        messages.error(request, "You are not authorized to edit this request.")
        return redirect('donations:donation_request_list') 
    total_donated = Donation.objects.filter(donation_request=donation_request).aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_amount = donation_request.amount_requested - total_donated if donation_request.amount_requested else None


    total_donated = Donation.objects.filter(donation_request=donation_request).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    remaining_amount = donation_request.amount_requested - total_donated if donation_request.amount_requested else None

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

    return render(request, 'donations/edit_donation_request.html', {
        'donation_request': donation_request,
        'total_donated': total_donated,
        'remaining_amount': remaining_amount
    })


def delete_donation_request(request, donation_id):
    donation_request = get_object_or_404(DonationRequest, id=donation_id)

    if request.user != donation_request.shelter.user:
        messages.error(request, "You are not authorized to delete this request.")
        return redirect('donations:donation_request_list')
    
    shelter_id = donation_request.shelter.id 
    donation_request.delete()
    messages.success(request, "Donation request has been successfully deleted.")
    return redirect('accounts:shelter_profile', shelter_id=shelter_id)

def make_medical_donation(request, donation_request_id):
    donation_request = get_object_or_404(DonationRequest, id=donation_request_id)

    total_donated = Donation.objects.filter(donation_request=donation_request).aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_amount = donation_request.amount_requested - total_donated if donation_request.donation_type == 'medical' else None
    is_fulfilled = (remaining_amount is not None) and (remaining_amount <= 0)

    if request.method == 'POST':
        donor_name = request.POST.get('donor_name', '')
        donation_type = request.POST.get('donation_type', '')
        amount = request.POST.get('amount', '')
        payment_method = request.POST.get('payment_method', '')
        payment_proof = request.FILES.get('payment_proof', None)

        if not amount or not payment_method:
            messages.error(request, "Amount and Payment Method are required for monetary donations.")
            return redirect('donations:make_medical_donation', donation_request_id=donation_request.id)

        try:
            amount = float(amount)
            if remaining_amount is not None and amount > remaining_amount:
                messages.error(request, f"The donation amount cannot exceed the remaining amount of {remaining_amount}.")
                return redirect('donations:make_medical_donation', donation_request_id=donation_request.id)
        except ValueError:
            messages.error(request, "Please enter a valid donation amount.")
            return redirect('donations:make_medical_donation', donation_request_id=donation_request.id)

        donation = Donation(
            donor_name=donor_name,
            donation_type=donation_type,
            amount=amount,
            payment_method=payment_method,
            donation_request=donation_request
        )

        if payment_proof:
            donation.payment_proof = payment_proof

        donation.save()

        messages.success(request, "Thank you for your monetary donation!")
        return redirect('donations:donation_request_list')  

    return render(request, 'donations/medical_donate.html', {
        'donation_request': donation_request,
        'is_fulfilled': is_fulfilled,
        'remaining_amount': remaining_amount
    })

def make_supply_donation(request, donation_request_id):
    donation_request = get_object_or_404(DonationRequest, id=donation_request_id)

    if request.method == 'POST':
        donor_name = request.POST.get('donor_name', '')
        donation_type = request.POST.get('donation_type', '')
        shipping_company = request.POST.get('shipping_company', '')
        tracking_number = request.POST.get('tracking_number', '')
        payment_proof = request.FILES.get('payment_proof', None)

        if not shipping_company or not tracking_number:
            messages.error(request, "Please provide both the shipping company and tracking number for supplies donation.")
            return redirect('donations:make_supply_donation', donation_request_id=donation_request.id)

        if request.POST.get('amount'):
            messages.error(request, "Monetary donations are not required for supplies donations.")
            return redirect('donations:make_supply_donation', donation_request_id=donation_request.id)

        donation = Donation(
            donor_name=donor_name,
            donation_type=donation_type,
            shipping_company=shipping_company,
            tracking_number=tracking_number,
            donation_request=donation_request
        )
        if payment_proof:
            donation.payment_proof = payment_proof
        donation.save()
        messages.success(request, "Thank you for your supplies donation!")
        return redirect('donations:donation_request_list')

    return render(request, 'donations/supply_donate.html', {
        'donation_request': donation_request,
    })

'''
def make_donation(request, donation_request_id):
    donation_request = get_object_or_404(DonationRequest, id=donation_request_id)

    total_donated = Donation.objects.filter(donation_request=donation_request).aggregate(Sum('amount'))['amount__sum'] or 0

    if donation_request.donation_type == 'medical' and donation_request.amount_requested:
        remaining_amount = donation_request.amount_requested - total_donated
    else:
        remaining_amount = None

    is_fulfilled = (remaining_amount is not None) and (remaining_amount <= 0)

    if request.method == 'POST':
        donor_name = request.POST.get('donor_name', '')
        donation_type = request.POST.get('donation_type', '')
        amount = request.POST.get('amount', '')
        payment_method = request.POST.get('payment_method', '')
        shipping_company = request.POST.get('shipping_company', '')
        tracking_number = request.POST.get('tracking_number', '')
        payment_proof = request.FILES.get('payment_proof', None)

        logger.debug(f"Donor Name: {donor_name}, Donation Type: {donation_type}, Shipping Company: {shipping_company}, Tracking Number: {tracking_number}")

        if donation_type == 'monetary':
            try:
                amount = float(amount)
                if remaining_amount is not None and amount > remaining_amount:
                    messages.error(request, f"The donation amount cannot exceed the remaining amount of {remaining_amount}.")
                    return redirect('donations:make_donation', donation_request_id=donation_request.id)
            except ValueError:
                messages.error(request, "Please enter a valid donation amount.")
                return redirect('donations:make_donation', donation_request_id=donation_request.id)

            if amount and payment_method:
                donation = Donation(
                    donor_name=donor_name,
                    donation_type=donation_type,
                    amount=amount,
                    payment_method=payment_method,
                    donation_request=donation_request
                )
                donation.save()
                messages.success(request, "Thank you for your monetary donation!")
                return redirect('donations:donation_request_list')
        
        elif donation_type == 'supplies':
            if not shipping_company or not tracking_number:
                messages.error(request, "Please provide both the shipping company and tracking number for supplies donation.")
                return redirect('donations:make_donation', donation_request_id=donation_request.id)

            if amount:
                messages.error(request, "Monetary donations are not required for supplies donations.")
                return redirect('donations:make_donation', donation_request_id=donation_request.id)

            donation = Donation(
                donor_name=donor_name,
                donation_type=donation_type,
                shipping_company=shipping_company,
                tracking_number=tracking_number,
                donation_request=donation_request
            )
            if payment_proof:
                donation.payment_proof = payment_proof
            donation.save()
            messages.success(request, "Thank you for your supplies donation!")
            return redirect('donations:donation_request_list')

        else:
            messages.error(request, "Please fill all required fields.")
            return redirect('donations:make_donation', donation_request_id=donation_request.id)

    return render(request, 'donations/donate.html', {
        'donation_request': donation_request, 
        'is_fulfilled': is_fulfilled,
        'remaining_amount': remaining_amount
    })'''