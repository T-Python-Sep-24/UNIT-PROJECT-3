from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpRequest, HttpResponse
from .forms import CardForm , FolderForm
from .models import Folder , Flashcard
from django.forms import modelformset_factory
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse
from django.contrib import messages

# Create your views here.

def home_views(request):
    top_users = User.objects.annotate(flashcard_count=Count('flashcards')).order_by('-flashcard_count')[:3]
    
    return render(request, 'main/home.html', {'top_users': top_users})

@login_required
def create_folder_views(request):
    if request.method == "POST":
        folder_form = FolderForm(request.POST)
        if folder_form.is_valid():
            folder = folder_form.save(commit=False)
            folder.user = request.user
            folder.save()
            messages.success(request, "Folder created successfully!")
            return redirect(reverse('cards:folder_detail', args=[folder.id]))
    else:
        folder_form = FolderForm()
    return render(request, "main/create_folder.html", {"folder_form": folder_form})

 
@login_required
def folder_list(request):
    folders = Folder.objects.filter(user=request.user, is_active=True)
    
    search_query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()
    
    if search_query:
        folders = folders.filter(name__icontains=search_query)
    
    valid_categories = dict(Folder.CATEGORY_CHOICES).keys()
    if category_filter and category_filter in valid_categories:
        folders = folders.filter(category=category_filter)
    
    paginator = Paginator(folders.order_by('-created_at'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    max_flashcards = 100 
    folders_with_ratios = []
    
    for folder in page_obj:
        flashcard_count = folder.flashcards.count()
        flashcard_ratio = min((flashcard_count / max_flashcards) * 100, 100)
        folders_with_ratios.append({
            'folder': folder,
        })
    
    context = {
        'folders': folders_with_ratios,
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'CATEGORY_CHOICES': Folder.CATEGORY_CHOICES,  
    }
    return render(request, 'main/folder_list.html', context)




@login_required
def create_flashcard_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    FlashcardFormSet = modelformset_factory(Flashcard, form=CardForm, extra=3)
    
    if request.method == 'POST':
        formset = FlashcardFormSet(request.POST, queryset=Flashcard.objects.none())
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    flashcard = form.save(commit=False)
                    flashcard.folder = folder
                    flashcard.user = request.user  
                    flashcard.save()
            messages.success(request, "Flashcards created successfully!")
            return redirect('cards:folder_detail', folder_id=folder.id)
    else:
        formset = FlashcardFormSet(queryset=Flashcard.objects.none())
    
    return render(request, 'main/create_flashcard.html', {'formset': formset, 'folder': folder})


@login_required
def folder_detail_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user, is_active=True)
    flashcards = folder.flashcards.all()
    return render(request, 'main/folder_detail.html', {'folder': folder, 'flashcards': flashcards})


def folder_delete_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    if request.method == 'POST':
        folder.delete()
        messages.success(request, "Folder deleted successfully!")
        return redirect('cards:folder_list')
    
    return render(request, 'main/folder_list.html', {'folder': folder})
