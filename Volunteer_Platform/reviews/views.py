from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from users.models import UserProfile

@login_required
def add_review(request, profile_id):
    reviewee = get_object_or_404(UserProfile, id=profile_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user.userprofile
            review.reviewee = reviewee
            review.save()
            return redirect('dashboard')
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form, 'reviewee': reviewee})
