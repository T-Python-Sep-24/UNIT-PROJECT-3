from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from .models import Blog
from main.models import Language
from .forms import BlogForm
from django.core.paginator import Paginator
# Create your views here.


def blogs_all_view(request:HttpRequest):
    blogs=Blog.objects.all()
    languages=Language.objects.all()
    if "search" in request.GET and len(request.GET["search"]) >= 1:
        blogs = blogs.filter(title__icontains=request.GET["search"])

    if "filter_by_lang" in request.GET and request.GET["filter_by_lang"]:
        blogs = blogs.filter(language__id=request.GET["filter_by_lang"])

    if "order_by" in request.GET and request.GET.get("date"):
        blogs = blogs.order_by("-created_at")
    
    p=Paginator(blogs,6)
    page=request.GET.get('page',1)
    blogs_list=p.get_page(page)

    return render(request,"blogs/blogs.html",{"blogs":blogs_list,"languages":languages})




def blog_details_view(request:HttpRequest,blog_id):
    blog =Blog.objects.get(pk=blog_id)
    
    if blog.url_video:
      url_id = blog.url_video.split("=")[-1]
    else:
       url_id = ''

    return render(request,"blogs/blog_details.html",{"blog":blog,"url_id":url_id})


def new_blog_view(request:HttpRequest):
   # if not request.user.is_superuser and not request.user.has_perm("cars.add_car"):
   #     messages.warning(request,"You don't have permission to add car","alert-warning")
   #     return redirect("main:home_view")
    languages=Language.objects.all()
    if request.method=="POST":
        blog_form=BlogForm(request.POST,request.FILES)
        if blog_form.is_valid():
              blog_form.save()
              messages.success(request, 'The blog has been added successfully!','alert-success')
              return redirect("blogs:new_blog_view")
        else:
            print("form is not valid")
            print(blog_form.errors)
    return render(request,'blogs/new_blog.html',{"languages":languages})


def update_blog_view(request:HttpRequest,blog_id):
    try:   
        #if not request.user.is_superuser:
         #   messages.warning(request,"only staff can update car","alert-warning")
          #  return redirect("main:home_view")
 
        blog =Blog.objects.get(pk=blog_id)
        languages=Language.objects.all()

        if request.method=="POST":
            blog_form=BlogForm(request.POST,request.FILES,instance=blog)
            if blog_form.is_valid():
                blog_form.save()
               
                messages.success(request, 'The blog has been updated successfully!','alert-success')
                return redirect("blogs:update_blog_view",blog_id=blog.id)
            else:
                print("form is not valid")
                print(blog_form.errors)
        else:   
            blog_form = BlogForm(instance=blog)        
        return render(request,'blogs/update_blog.html',{"blog":blog,"languages":languages})
    except Blog.DoesNotExist:
        print("error massege")
        messages.error(request, "An error occurred: The page not found",'alert-danger')
        return redirect('main:home_view')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('main:home_view')

def delete_blog_view(request,blog_id):
    try:
        #if not request.user.is_superuser:
         #   messages.warning(request,"only staff can delete car","alert-warning")
          #  return redirect("main:home_view")

        blog=Blog.objects.get(pk=blog_id)
        blog.delete()
        messages.success(request, 'The blog has been deleted successfully!','alert-success')
        return redirect("main:home_view")
    except Blog.DoesNotExist:
        print("error massege")
        messages.error(request, "An error occurred: The page not found",'alert-danger')
        return redirect('main:home_view')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}",'alert-danger')
        return redirect('main:home_view')
