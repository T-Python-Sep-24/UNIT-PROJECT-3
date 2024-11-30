from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Place, Bookmark
from .forms import PlaceForm


def all_places_view(request):
    """
    Display a list of all places, with optional filtering by category and search query.
    """
    try:
        category = request.GET.get('category', None)
        query = request.GET.get('q', None)
        places = Place.objects.all()

        if query:
            places = places.filter(Q(name__icontains=query) | Q(city__icontains=query))
        if category:
            places = places.filter(category=category)

        # Fetch category choices from the model
        category_choices = Place.CATEGORY_CHOICES

        return render(request, 'places/all_places.html', {
            'places': places,
            'category_choices': category_choices,
            'query': query,
            'category': category,
        })

    except Place.DoesNotExist:
        messages.error(request, "An error occurred: Some places could not be found.")
        return render(request, 'places/all_places.html', {
            'places': [],
            'category_choices': Place.CATEGORY_CHOICES,
            'query': query,
            'category': category,
        })

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}")
        return render(request, 'places/all_places.html', {
            'places': [],
            'category_choices': Place.CATEGORY_CHOICES,
            'query': query,
            'category': category,
        })

def place_detail_view(request, pk):
    """
    Display details of a specific place.
    """
    try:
        place = Place.objects.get(pk=pk)
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
        return redirect('places:all_places_view')
    except Exception as e:
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
        messages.success(request, "Place deleted successfully!")
        return redirect('places:all_places_view')
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('places:all_places_view')


def search_view(request):
    """
    Search for places by name, city, or category.
    """
    try:
        query = request.GET.get('q', '').strip()
        category = request.GET.get('category', '').strip()
        results = Place.objects.all()

        if query:
            results = results.filter(Q(name__icontains=query) | Q(city__icontains=query))

        if category:
            results = results.filter(category=category)

        # Fetch category choices from the model
        category_choices = Place.CATEGORY_CHOICES

        return render(request, 'places/search.html', {
            'results': results,
            'query': query,
            'category': category,
            'category_choices': category_choices,
        })

    except Place.DoesNotExist:
        messages.error(request, "An error occurred: Some places could not be found.")
        return render(request, 'places/search.html', {
            'results': [],
            'query': query,
            'category': category,
            'category_choices': Place.CATEGORY_CHOICES,
        })

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}")
        return render(request, 'places/search.html', {
            'results': [],
            'query': query,
            'category': category,
            'category_choices': Place.CATEGORY_CHOICES,
        })


@login_required
def add_bookmark_view(request, place_id):
    """
    Toggle bookmark for a specific place.
    """
    try:
        place = get_object_or_404(Place, pk=place_id)
        bookmark = Bookmark.objects.filter(place=place, user=request.user).first()

        if not bookmark:
            Bookmark.objects.create(user=request.user, place=place)
            messages.success(request, "Bookmark added successfully!")
        else:
            bookmark.delete()
            messages.warning(request, "Bookmark removed.")
        return redirect('places:place_detail_view', pk=place_id)
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('places:place_detail_view', pk=place_id)
