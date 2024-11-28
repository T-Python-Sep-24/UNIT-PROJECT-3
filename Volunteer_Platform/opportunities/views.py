from django.shortcuts import render

# Create your views here.

def opportunity_list(request):
    return render(request, 'opportunities/opportunity_list.html')
