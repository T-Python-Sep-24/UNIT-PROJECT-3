from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .forms import RecipeForm

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'main/index.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'main/recipe_detail.html', {'recipe': recipe})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
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
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('main:recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'main/update_recipe.html', {'form': form})

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        recipe.delete()
        return redirect('main:index')
    return render(request, 'main/delete_recipe.html', {'recipe': recipe})

def search(request):
    query = request.GET.get('q', '')
    recipes = Recipe.objects.filter(title__icontains=query)
    return render(request, 'main/search.html', {'recipes': recipes, 'query': query})
