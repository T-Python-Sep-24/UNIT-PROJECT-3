from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .models import Fund, Review
from accounts.models import Bookmark, UserMessage
from payments.models import Wallet

from datetime import datetime, timedelta, date


# Create your views here.


def all_funds_view(request: HttpRequest):

    funds = Fund.objects.all()

    if 'keyword' in request.GET:

        keyword = request.GET['keyword']
        funds = funds.filter(fund_name__contains = keyword)

    if 'order_by' in request.GET:

        if request.GET['order_by'] == 'newest':
            funds = funds.order_by('-created_at')
        elif request.GET['order_by'] == 'oldest':
            funds = funds.order_by('created_at')

    if 'availability' in request.GET:
        if not request.GET['availability'] == 'all':
            funds = funds.filter(is_available = request.GET['availability'])
    if 'privacy' in request.GET:
        if not request.GET['privacy'] == 'all':
            funds = funds.filter(fund_privacy = request.GET['privacy'])

    paginator = Paginator(funds, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'all_funds.html', context={'funds': funds, 'page_obj': page_obj})


def fund_details_view(request: HttpRequest, fund_id):

    fund = Fund.objects.get(pk=fund_id)
    reviews = Review.objects.filter(fund=fund)

    is_bookmarked = Bookmark.objects.filter(fund=fund, user=request.user).exists() if request.user.is_authenticated else False

    return render(request, 'fund_details.html', context={'is_bookmarked':is_bookmarked, 'fund':fund, 'reviews':reviews, 'rates':Review.Rates.choices})


def user_funds_view(request: HttpRequest):

    if not request.user.is_authenticated:
        messages.error(request, "Register to create new Fund", 'alert-danger')
        return redirect('accounts:sign_in')

    funds = Fund.objects.filter(fund_owner = request.user)
    return render(request, 'user_funds.html', context={'funds':funds})


def user_participated_in_funds_view(request: HttpRequest):

    if not request.user.is_authenticated:
        messages.error(request, "Register to create new Fund", 'alert-danger')
        return redirect('accounts:sign_in')

    funds = Fund.objects.filter(fund_members = request.user)
    return render(request, 'user_participated_in_funds.html', context={'funds':funds})


def add_fund_view(request: HttpRequest):

    members = User.objects.all()

    if not request.user.is_authenticated:
        messages.error(request, "Register to create new Fund", 'alert-danger')
        return redirect('accounts:sign_in')
    try:

        if request.method == "POST":
            new_fund = Fund(
                fund_owner = request.user,
                # fund_members = request.POST.getlist('members'),
                fund_name = request.POST['fund_name'],
                about = request.POST['about'],
                policies = request.POST['policies'],
                monthly_stock = request.POST['monthly_stock'],
                hold_duration = request.POST['hold_duration'],

            )
            if 'fund-privacy' in request.POST:
                new_fund.fund_privacy = True
            else:
                new_fund.fund_privacy = False
            if 'fund-status' in request.POST:
                new_fund.is_available = True
            else:
                new_fund.is_available = False

            new_fund.receiving_month = len(request.POST.getlist('members'))
            new_fund.save()
            new_fund.fund_members.set(request.POST.getlist('members'))

            for member_id in request.POST.getlist('members'):
                member = User.objects.get(pk=member_id)

            # Send message to user
                new_user_message = UserMessage(
                    sender = request.user,
                    user = member,
                    subject = 'Added to Fund',
                    content = f'You Were Enrolled in a Fund by {request.user.username}',
                )
                new_user_message.save()

            messages.success(request, "fund was added successfully", "alert-success")

            # Send message to user
            new_user_message = UserMessage(
                sender = User.objects.get(pk=1),
                user = request.user,
                subject = 'Add Fund',
                content = 'You Added New Fund',
            )
            new_user_message.save()

            return redirect("funds_app:all_funds_view")

        return render(request, 'add_fund.html', context={'members': members})
    except Exception as e:
        print(e)
        messages.error(request, "Error adding fund", "alert-danger")
        return redirect(request, 'funds_app:all_funds_view')


def update_fund_view(request: HttpRequest,fund_id):

    if not (request.user.is_superuser or request.user.is_authenticated):
        messages.error(request, "Only Authorized Uses Can update funds", 'alert-danger')
        return redirect('funds_app:fund_details_view', fund_id=fund_id)

    try:

        fund = Fund.objects.get(pk=fund_id)
        members = User.objects.all()

        if request.method == "POST":
            with transaction.atomic():
                fund.fund_name = request.POST['fund_name']
                fund.about = request.POST['about']
                fund.policies = request.POST['policies']
                fund.monthly_stock = request.POST['monthly_stock']
                fund.hold_duration = request.POST['hold_duration']
                fund.receiving_month = len(request.POST.getlist('members'))
                fund.save()

                fund.fund_members.set(request.POST.getlist('members'))

                for member_id in request.POST.getlist('members'):
                    member = User.objects.get(pk=member_id)
                    # Send message to user
                    new_user_message = UserMessage(
                        sender = request.user,
                        user = member,
                        subject = 'Updating Fund',
                        content = f'A fund you are Enrolled in were updated by the fund owner ({request.user.username})',
                    )
                    new_user_message.save()

                if 'fund-privacy' in request.POST and request.POST['fund-privacy'] == 'on':
                    print(request.POST['fund-privacy'])
                    fund.fund_privacy = False
                else:
                    fund.fund_privacy = True
                if 'fund-status' in request.POST and request.POST['fund-status'] == 'on':
                    print(request.POST['fund-status'])
                    fund.is_available = True
                else:
                    fund.is_available = False

                # Send message to user
                new_user_message = UserMessage(
                    sender = User.objects.get(pk=1),
                    user = request.user,
                    subject = 'Update Fund',
                    content = 'You Updated a Fund',
                )
                fund.save()
                new_user_message.save()
                messages.success(request, "fund was Updated successfully", "alert-success")
                return redirect("funds_app:fund_details_view", fund_id = fund_id)

        return render(request, 'update_fund.html', context={'fund':fund, 'members': members})

    except Exception as e:

        print(e)
        messages.error(request, "Error adding fund", "alert-danger")
        return redirect(request, 'funds_app:all_funds_view')


def delete_fund_view(request: HttpRequest, fund_id):

    if request.user.is_superuser or request.user.is_authenticated:
        fund = Fund.objects.get(pk=fund_id)
        fund.delete()
        # Send message to user
        new_user_message = UserMessage(
            sender = User.objects.get(pk=1),
            user = request.user,
            subject = 'Delete Fund',
            content = 'You Deleted a Fund',
        )
        new_user_message.save()
        messages.success(request, 'Fund was deleted successfully', 'alert-success')
    return redirect('funds_app:all_funds_view')


def add_review_view(request: HttpRequest, fund_id):

    try:
        if not request.user.is_authenticated:
            messages.error(request, "Please Login to add reviews", 'alert-danger')
            return redirect('accounts:sign_in')
        if request.method == 'POST':
            new_comment = Review(
                fund=Fund.objects.get(pk=fund_id),
                user=request.user,
                comment=request.POST['comment'],
                rating=request.POST['rating'])
            new_comment.save()

            # Send message to user
            new_user_message = UserMessage(
                sender = User.objects.get(pk=1),
                user = request.user,
                subject = 'Review Fund',
                content = 'You Reviewed a Fund',
            )

            new_user_message.save()
            messages.success(request, 'Comment was added successfully', 'alert-success')
        return redirect('funds_app:fund_details_view', fund_id = fund_id)
    except Exception as e:
        messages.error(request, 'Error in adding your comment', 'alert-danger')
        return render(request,'page_not_found.html')
        print(e)


def delete_review_view(request: HttpRequest, review_id):

    if request.user.is_superuser:
        review = Review.objects.get(pk=review_id)
        review.delete()

        # Send message to user
        new_user_message = UserMessage(
            sender = User.objects.get(pk=1),
            user = request.user,
            subject = 'Delete Review',
            content = 'You Deleted your review',
        )

        new_user_message.save()
        messages.success(request, 'Review Deleted Successfully', 'alert-success')
    return redirect('funds_app:fund_details_view', fund_id=review.fund.id)


def add_bookmark_view(request: HttpRequest, fund_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please register to add bookmark', 'alert-danger')
        return redirect('accounts:sign_in')

    try:
        fund = Fund.objects.get(pk=fund_id)

        new_bookmark = Bookmark(
            user = request.user,
            fund = fund
        )
        bookmark = Bookmark.objects.filter(fund=fund, user=request.user)

        if not bookmark:
            new_bookmark.save()
            messages.success(request, 'bookmark added', 'alert-success')
        else:
            bookmark.delete()
            messages.success(request, 'bookmark removed', 'alert-warning')

    except Exception as e:
        print(e)

    return redirect(request.GET.get('next', '/'))


def fund_participate_view(request: HttpRequest, fund_id):

    if not request.user.is_authenticated:
        messages.error(request, "Register to Participate in Funds", 'alert-danger')
        return redirect('accounts:sign_in')

    if not request.user.wallet:
        messages.error(request, "Add Wallet to Participate in Funds", 'alert-danger')
        return redirect('payments:add_wallet')

    fund = Fund.objects.get(pk=fund_id)
    wallet = request.user.wallet

    try:
        if fund.is_available and wallet.balance >= 3000:
            with transaction.atomic():

                fund.fund_members.add(request.user.id)
                fund.receiving_month += 1
                fund.save()

                # Send message to user
                wallet.balance -= fund.monthly_stock
                wallet.save()
                new_user_message = UserMessage(
                    sender = User.objects.get(pk=1),
                    user = request.user,
                    subject = 'Enroll in Fund ',
                    content = f'You Enrolled in a Fund {fund.fund_name} and substitute {fund.monthly_stock} form your wallet',
                )
                new_user_message.save()
                messages.success(request, "Your Participated in this Fund successfully", "alert-success")

        elif wallet.balance < 3000:
            messages.warning(request, "Your wallet Balance doesn't meet the minimum requirement for enrolling in funds", 'alert-warning')
            return redirect('funds_app:all_funds_view')
        else:
            messages.warning(request, "This Fund is Not available for participation", 'alert-warning')
            return redirect('funds_app:all_funds_view')
        return redirect('funds_app:all_funds_view')

    except Exception as e:
        print(e)
        messages.error(request, "couldn't Participate in this Fund", "alert-danger")


def start_fund(request: HttpRequest, fund_id):

    fund = Fund.objects.get(pk=fund_id)

    if not request.user.is_authenticated:
        messages.error(request, "Register to start in Funds", 'alert-danger')
        return redirect('accounts:sign_in')

    if not request.user == fund.fund_owner:
        messages.error(request, "Fund Owners only cat start their", 'alert-danger')
        return redirect('funds_app:fund_details_view', fund_id = fund_id)

    try:

        if request.user.is_authenticated and request.user == fund.fund_owner:
            with transaction.atomic():
                fund.start_date = datetime.now()
                fund.is_available = False
                fund.save()

            for member_id in request.POST.getlist('members'):
                member = User.objects.get(pk=member_id)
                # Send message to user
                new_user_message = UserMessage(
                    sender = fund.fund_owner,
                    user = member,
                    subject = 'Start Funding',
                    content = f'the fund {fund.fund_name} you are Enrolled started, Date:({fund.start_date})',
                )
                new_user_message.save()
                # Send message to fund members
                new_user_message = UserMessage(
                    sender = User.objects.get(pk=1),
                    user = request.user,
                    subject = 'Update Fund',
                    content = 'You Updated a Fund',
                )

                new_user_message.save()
                messages.success(request, "fund was Updated successfully", "alert-success")
            return redirect('funds_app:fund_details_view', fund_id=fund_id)
    except Exception as e:
        print(e.__cause__)
        return render(request, 'index.html')

def payment_schedule(request, fund_id):

    fund = Fund.objects.get(pk=fund_id, fund_members=request.user)

    total_members = fund.fund_members.count()
    monthly_stock = fund.monthly_stock
    user_receive_month = fund.receiving_month

    schedule = []
    start_date = fund.start_date

    for month in range(total_members):
        payment_date = start_date + timedelta(days=30*month)
        amount = monthly_stock
        is_receiving = month + 1 == user_receive_month

        schedule.append({
            'month': month + 1,
            'date': payment_date,
            'amount': amount,
            'is_receiving': is_receiving
        })

    context = {
        'schedule': schedule,
        'fund': fund,
        'total_amount': monthly_stock * total_members,
        'current_date': datetime.now()
    }

    return render(request, 'fund_payments_schedule.html', context)