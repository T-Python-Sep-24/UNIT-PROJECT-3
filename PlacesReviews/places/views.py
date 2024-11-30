from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Place, Bookmark
from .forms import PlaceForm


def all_places_view(request):
    """
    Display a list of all places.
    """
    try:
        places = Place.objects.all()
        return render(request, 'places/all_places.html', {'places': places})
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('main:home_view')


def place_detail_view(request, pk):
    try:
        print(f"Fetching place with ID: {pk}")
        place = Place.objects.get(pk=pk)
        print(f"Place found: {place}")

        can_delete = request.user.is_authenticated and (place.author == request.user or request.user.is_staff)
        is_bookmarked = (
            request.user.is_authenticated
            and Bookmark.objects.filter(place=place, user=request.user).exists()
        )

        return render(request, 'places/place_detail.html', {
            'place': place,
            'can_delete': can_delete,
            'is_bookmarked': is_bookmarked,
        })

    except Place.DoesNotExist:
        messages.error(request, "The requested place does not exist.")
        print("Place.DoesNotExist: Redirecting to All Places.")
        return redirect('places:all_places_view')

    except Exception as e:
        print(f"Unexpected error in place_detail_view: {e}")
        messages.error(request, f"An error occurred: {e}")
        return redirect('places:all_places_view')

@login_required
def add_place_view(request):
    """
    Allow authenticated users to add a new place.
    """
    try:
        if request.method == 'POST':
            form = PlaceForm(request.POST, request.FILES)
            if form.is_valid():
                place = form.save(commit=False)
                place.author = request.user
                place.save()
                messages.success(request, "Place added successfully!")
                return redirect('places:all_places_view')
            else:
                messages.error(request, "Failed to add the place. Please try again.")
        else:
            form = PlaceForm()
        return render(request, 'places/add_place.html', {'form': form})
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('places:all_places_view')


def search_view(request):
    """
    Allow users to search for places by name or city.
    """
    try:
        query = request.GET.get('q', '')
        results = Place.objects.filter(Q(name__icontains=query) | Q(city__icontains=query))
        return render(request, 'places/search.html', {'results': results, 'query': query})
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('places:all_places_view')



@login_required
def delete_place_view(request, pk):
    """
    Allow the author or an admin to delete a place.
    """
    try:
        place = get_object_or_404(Place, pk=pk)

        if place.author != request.user and not request.user.is_staff:
            messages.error(request, "You are not authorized to delete this place.")
            return redirect('places:place_detail_view', pk=pk)

        place.delete()
        return redirect('places:all_places_view')
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('places:all_places_view')


@login_required
def add_bookmark_view(request, place_id):
    """
    Toggle bookmark for a specific place.
    """
    try:
        place = get_object_or_404(Place, pk=place_id)
        bookmark = Bookmark.objects.filter(place=place, user=request.user).first()

        if not bookmark:
            new_bookmark = Bookmark(user=request.user, place=place)
            new_bookmark.save()
            messages.success(request, "Bookmark added successfully!", "alert-success")
        else:
            bookmark.delete()
            messages.warning(request, "Bookmark removed.", "alert-warning")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}", "alert-danger")

    return redirect('places:place_detail_view', pk=place_id)

print(Place.objects.all())  # Check all Place objects
print(Place.objects.get(pk=1))  # Ensure a Place with pk=1 exists
