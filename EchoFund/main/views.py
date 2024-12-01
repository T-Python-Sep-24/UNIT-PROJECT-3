from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from funds_app.models import Fund
from .forms import ContactForm
from .models import Contact, Testimonial


# Create your views here.

def home_view(request: HttpRequest):

    funds = Fund.objects.all()[:3]
    testimonials = Testimonial.objects.all()
    return render(request, 'index.html', context={'funds': funds, 'testimonials': testimonials})


def search_view(request: HttpRequest):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        funds = Fund.objects.filter(
            Q(fund_name__contains=keyword) |
            Q(about__contains=keyword) |
            Q(policies__contains=keyword) |
            Q(monthly_stock__contains=keyword) |
            Q(hold_duration__contains=keyword) |
            Q(created_at__contains=keyword)
        )
    else:
        funds = []

    return render(request, 'search_results.html', context={'funds':funds})


def contact_view(request: HttpRequest):

    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Message was sent Successfully', 'alert-success')
            return redirect('main:home_view')
        else:
            print('Form is not valid')
            print(contact_form.errors)
            messages.error(request, 'Error in sending the Message', 'alert-danger')
    return redirect('main:home_view')


def rate_us_view(request: HttpRequest):

    if request.method == 'POST':
        if request.user.is_authenticated:
            new_rate = Testimonial(

                name=request.POST['name'],
                subject=request.POST['subject'],
                comment=request.POST['comment'],
                rating=request.POST['rating'],
                image=request.user.profile.avatar
            )
        else:
            new_rate = Testimonial(

                name=request.POST['name'],
                image=request.FILES['image'],
                subject=request.POST['subject'],
                comment=request.POST['comment'],
                rating=request.POST['rating'])

        new_rate.save()
        messages.success(request, 'Thank You for rating us', 'alert-success')
        return redirect('main:home_view')

    # messages.error(request, 'Error in adding your comment', 'alert-danger')
    # return render(request,'page_not_found.html')
    # print(e)

    return render(request, 'rate_us.html', context={'rates': Testimonial.Rates.choices})
