from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from accounts.models import UserMessage
from .models import Wallet
# Create your views here.


def add_wallet(request: HttpRequest):

    if not request.user.is_authenticated:
        messages.error(request, 'Sign in To add new Wallet')
        return redirect('accounts:sign_in')
    try:
        if request.method == "POST":
            with transaction.atomic():
                new_wallet = Wallet(
                    user = request.user,
                    balance = request.POST['balance'],
                    pin_number = request.POST['pin_number'],
                )
                new_wallet.save()

                # Send message to user
                new_user_message = UserMessage(
                    sender = User.objects.get(pk=1),
                    user = request.user,
                    subject = 'Delete Fund',
                    content = 'You Added a new wallet',
                )
                new_user_message.save()

            messages.success(request, 'Wallet was added Successfully', 'alert-success')
            return redirect('accounts:profile_view', user_name=request.user.username)
        return render(request, 'add_wallet.html')
    except Exception as e:
        print(e)
        messages.error(request, 'Error in adding your wallet', 'alert-danger')
        return redirect('accounts:profile_view', user_name=request.user.username)

def wallet_details(request: HttpRequest, wallet_id):

    wallet = Wallet.objects.get(pk=wallet_id)
    return render(request, 'wallet_details.html', context={'wallet': wallet})


def update_wallet(request: HttpRequest, wallet_id):

    if not request.user.is_authenticated:
        messages.error(request, "Sign in to update your wallet","alert-warning")
        return redirect("accounts:sign_in")

    wallet = Wallet.objects.get(pk=wallet_id)
    if request.method == "POST":
        try:
            with transaction.atomic():
                wallet.balance = request.POST['balance']
                wallet.pin_number = request.POST['pin_number']
                wallet.save()
                # Send message to user
                new_user_message = UserMessage(
                    sender = User.objects.get(pk=1),
                    user = request.user,
                    subject = 'Delete Fund',
                    content = 'You Updated Your wallet',
                )
                new_user_message.save()
                messages.success(request, 'Wallet was updated successfully', 'alert-success')


                return redirect('payments:wallet_details', wallet_id=wallet_id)

        except Exception as e:
            print(e)
            messages.error(request, 'Error updating wallet', 'alert-danger')
    return render(request, 'update_wallet.html', context={'wallet':wallet})


def delete_wallet(request:HttpRequest, wallet_id):
    try:
        if request.user.is_authenticated:
            with transaction.atomic():
                wallet = Wallet.objects.get(pk=wallet_id)
                wallet.delete()

                # Send message to user
                new_user_message = UserMessage(
                    sender = User.objects.get(pk=1),
                    user = request.user,
                    subject = 'Delete Fund',
                    content = 'You Deleted a Fund',
                )
                new_user_message.save()
        messages.success(request, 'wallet was deleted Successfully')
        return redirect('accounts:profile_view', request.user.username)
    except Exception as e:
        print(e)
        messages.error(request, 'Error Deleting Wallet', 'alert-danger')
        return redirect('payments:wallet_details', wallet_id=wallet_id)

