from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Language
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.


def home_view(request:HttpRequest):
    return render(request,"main/home.html")


def add_language_view(request:HttpRequest):

    if request.method=="POST":
        language=Language(name=request.POST["name"],native_name=request.POST["native_name"])
        language.save()
        messages.success(request,"The language added successfully","alert-success")
        return redirect("main:add_language_view")
    return render(request,"main/add_language.html")



def search_language(request):
   # if not request.user.is_superuser and not request.user.has_perm("cars.view_color"):
   #         messages.warning(request,"only staff can search color","alert-warning")
    #        return redirect("main:home_view")
    lang_name = request.GET.get('search', '') 

    if lang_name:
        try:
            lang = Language.objects.get(name__iexact=lang_name) 
            return redirect('main:update_language_view', lang_id=lang.id) 
        except Language.DoesNotExist:
            messages.error(request, 'Language name not found.','alert-danger')
            return redirect('main:home_view') 
    else:
        messages.error(request, 'Please enter a language name to search.','alert-danger')
        return redirect('main:home_view')
    

def update_language_view(request:HttpRequest,lang_id):
    try:
        lang = Language.objects.get(pk=lang_id)

        if request.method == "POST":
            lang.name = request.POST.get("name", lang.name)
            lang.native_name = request.POST.get("native_name", lang.native_name)
            lang.save()
            messages.success(request, "The language updated successfully", "alert-success")
            return redirect("main:update_language_view", lang_id=lang.id)

        else:
            return render(request, 'main/edit_language.html', {"language": lang})

    except Language.DoesNotExist:
        messages.error(request, "The requested language does not exist.", "alert-danger")
        return redirect('main:home_view')

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}", "alert-danger")
        return redirect('main:home_view')

def delete_language_view(request,lang_id):
    try:
#        if not request.user.is_superuser:
 #           messages.warning(request,"only staff can delete color","alert-warning")
  #          return redirect("main:home_view")
 
        lang=Language.objects.get(pk=lang_id)
        lang.delete()
        messages.success(request, 'The language has been deleted successfully!','alert-success')
        return redirect("main:home_view")
    except Language.DoesNotExist:
        print("error massege")
        messages.error(request, "An error occurred: The page not found",'alert-danger')
        return redirect('main:home_view')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}",'alert-danger')
        return redirect('main:home_view')
    