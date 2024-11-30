from django.shortcuts import render
from places.models import Place


def home_view(request):
    # Fetch the last 10 places ordered by creation date (descending)
    places = Place.objects.order_by('-created_at')[:5]
    return render(request, 'main/home.html', {'places': places})