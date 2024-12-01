from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Recipe, Review
from .forms import RecipeForm, ReviewForm

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'main/index.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    reviews = Review.objects.filter(recipe=recipe).order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe
            review.user = request.user
            review.save()
            return redirect('main:recipe_detail', recipe_id=recipe.id)
    else:
        form = ReviewForm()

    return render(request, 'main/recipe_detail.html', {
        'recipe': recipe,
        'reviews': reviews,
        'form': form
    })
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            return redirect('main:index')
    else:
        form = RecipeForm()
    return render(request, 'main/add_recipe.html', {'form': form})

@login_required
def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.created_by != request.user:
        return HttpResponseForbidden("You do not have permission to edit this recipe.")
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('main:recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'main/update_recipe.html', {'form': form, 'recipe':recipe})

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.created_by != request.user:
        return HttpResponseForbidden("You do not have permission to delete this recipe.")
    if request.method == 'POST':
        recipe.delete()
        return redirect('main:index')
    return render(request, 'main/delete_recipe.html', {'recipe': recipe})

def search(request):
    query = request.GET.get('q', '')
    recipes = Recipe.objects.filter(title__icontains=query)
    return render(request, 'main/search.html', {'recipes': recipes, 'query': query})
