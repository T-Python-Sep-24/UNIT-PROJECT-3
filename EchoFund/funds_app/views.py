from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Fund, Review
from accounts.models import Bookmark
# Create your views here.
def all_funds_view(request: HttpRequest):

    funds = Fund.objects.all()

    paginator = Paginator(funds, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'all_funds.html', context={'funds': funds, 'page_obj': page_obj})


def fund_details_view(request: HttpRequest, fund_id):

    fund = Fund.objects.get(pk=fund_id)
    reviews = Review.objects.filter(fund=fund)

    is_bookmarked = Bookmark.objects.filter(fund=fund, user=request.user).exists() if request.user.is_authenticated else False

    return render(request, 'fund_details.html', context={'is_bookmarked':is_bookmarked, 'fund':fund, 'reviews':reviews, 'rates':Review.Rates.choices})


def add_fund_view(request: HttpRequest):

    if not request.user.is_authenticated:
        messages.error(request, "Register to create new Fund", 'alert-danger')
        return redirect('accounts:sign_in')
    try:

        if request.method == "POST":
            new_fund = Fund(
                # founder = request.user
                # fund_members = request.POST.getlist('members')
                fund_name = request.POST['fund_name'],
                about = request.POST['about'],
                policies = request.POST['policies'],
                monthly_stock = request.POST['monthly_stock'],
                hold_duration = request.POST['hold_duration'],

            )
            new_fund.save()

            messages.success(request, "fund was added successfully", "alert-success")
            return redirect("funds_app:all_funds_view")
        # if request.method == "POST":
        #     car_brand = Brand.objects.filter(name=request.POST['brand'])
        #     car_form = CarForm(request.POST,car_brand, request.FILES)
        #     if car_form.is_valid():
        #         car_form.save()
        #         messages.success(request, "Car was added successfully", "alert-success")
        #         return redirect(request, "cars:all_cars_view")
        #     else:
        #         print("add car form is not valid")
        #         print(request.POST)
        #         print(car_form.errors)
        #         messages.error(request, "Error in adding car", "alert-danger")
        return render(request, 'add_fund.html')
    except Exception as e:
        print(e)
        messages.error(request, "Error adding fund", "alert-danger")
        return redirect(request, 'funds_app:all_funds_view')



def update_fund_view(request: HttpRequest):
    return None

def delete_fund_view(request: HttpRequest, fund_id):

    if request.user.is_superuser:
        fund = Fund.objects.get(pk=fund_id)
        fund.delete()
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

    return redirect('funds_app:fund_details_view', fund_id = fund_id)