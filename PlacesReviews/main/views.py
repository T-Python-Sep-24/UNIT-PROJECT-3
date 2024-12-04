from django.shortcuts import render
from places.models import Place


def home_view(request):
    """
    Renders the home page with the latest 5 places.

    Retrieves the 5 most recent `Place` objects, ordered by `created_at` in descending order. 
    Handles cases where no places exist or other errors occur.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders 'main/home.html' with a context containing `places`.
    """
    try:
        places = Place.objects.order_by('-created_at')[:5]
    except Exception as e:
        places = [] 
        print(f"An error occurred: {e}")

    return render(request, 'main/home.html', {'places': places})