from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from .models import Blog,Comment,ChallengeQuestion
from main.models import Language
from accounts.models import Bookmark
from .forms import BlogForm,ChallengeQuestionForm
from django.core.paginator import Paginator
# Create your views here.


def blogs_all_view(request:HttpRequest):
    blogs=Blog.objects.all()
    languages=Language.objects.all()
    challenge_question=ChallengeQuestion.objects.first()
    result=False
    if "search" in request.GET and len(request.GET["search"]) >= 1:
        blogs = blogs.filter(title__icontains=request.GET["search"])

    if "filter_by_lang" in request.GET and request.GET["filter_by_lang"]:
        blogs = blogs.filter(language__id=request.GET["filter_by_lang"])

    if "order_by" in request.GET and request.GET.get("date"):
        blogs = blogs.order_by("-created_at")
    
    if "answer" in request.POST and request.POST["answer"]:
        print("ansewr: ",request.POST["answer"])
        if challenge_question.correct_answer == request.POST["answer"]:
            result=True


    p=Paginator(blogs,6)
    page=request.GET.get('page',1)
    blogs_list=p.get_page(page)

    return render(request,"blogs/blogs.html",{"blogs":blogs_list,"languages":languages,
                                              "challenge_question":challenge_question,
                                              "result":result})




def blog_details_view(request:HttpRequest,blog_id):
    blog =Blog.objects.get(pk=blog_id)
    comments = Comment.objects.filter(blog=blog_id).order_by('-created_at')
    is_bookmarked=  Bookmark.objects.filter(blog=blog, user=request.user).exists() if request.user.is_authenticated else False

    if blog.url_video:
      url_id = blog.url_video.split("=")[-1]
    else:
       url_id = ''

    return render(request,"blogs/blog_details.html",{"blog":blog,"url_id":url_id,"comments":comments,"is_bookmarked":is_bookmarked})


def new_blog_view(request:HttpRequest):
    if not request.user.is_superuser and not request.user.has_perm("blogs.add_blog"):
       messages.warning(request,"You don't have permission to add blog","alert-warning")
       return redirect("main:home_view")
    languages=Language.objects.all()
    if request.method=="POST":
        blog_form=BlogForm(request.POST,request.FILES)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)  #don't save yet
            
            blog.written_by = request.user  
            blog.save()#now save it
            messages.success(request, 'The blog has been added successfully!','alert-success')
            return redirect("blogs:new_blog_view")
        else:
            print("form is not valid")
            print(blog_form.errors)
    return render(request,'blogs/new_blog.html',{"languages":languages})


def update_blog_view(request:HttpRequest,blog_id):
    try:   
        if not request.user.is_superuser and not request.user.has_perm("blogs.change_blog"):
            messages.warning(request,"You don't have permission to edit blog","alert-warning")
            return redirect("main:home_view")
 
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
        if not request.user.is_superuser and not request.user.has_perm("blogs.delete_blog"):
            messages.warning(request,"You don't have permission to edit blog","alert-warning")
            return redirect("main:home_view")

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

def add_comment_view(request:HttpRequest,blog_id):
    if not request.user.is_authenticated:
        messages.error(request,"only registed user can add comment",'alert-danger')
        return redirect("accounts:sign_in")
    if request.method=="POST":
        blog_obj = Blog.objects.get(pk=blog_id)
        comment=Comment(user=request.user,comment=request.POST['comment'],blog=blog_obj)
        comment.save()
        messages.success(request, "Thank you for your comment",'alert-success')
    return redirect("blogs:blog_details_view",blog_id=blog_id)    




def delete_comment_view(request:HttpRequest,comment_id):
    try:
            if not ((request.user.is_authenticated and  request.user == request.user) or request.user.is_superuser) :
                    messages.error(request,"only user can delete comment",'alert-danger')
                    return redirect("accounts:sign_in")


            comment = Comment.objects.get(pk=comment_id)
            blog_id=comment.blog.id
            comment.delete()
            messages.success(request, "comment deleted successfully",'alert-success')
            return redirect("blogs:blog_details_view",blog_id=blog_id)  
    except Comment.DoesNotExist:
        messages.error(request, "The comment does not exist", 'alert-danger')
        return redirect("blogs:blog_details_view",blog_id=blog_id)
    
    except Exception as e:
        print(e)
        messages.error(request, "An error occurred while trying to delete the comment", 'alert-danger')
        return redirect("blogs:blog_details_view",blog_id=blog_id)


def add_bookmark_view(request,blog_id):
    if not request.user.is_authenticated:
            messages.warning(request,"only rigisted user can save blogs","alert-warning")
            return redirect("accounts:sign_in")

    try:
       blog=Blog.objects.get(pk=blog_id)
       bookmark =Bookmark.objects.filter(user=request.user,blog=blog).first()
       if not bookmark:
            new_bookmark= Bookmark(user=request.user,blog=blog)
            new_bookmark.save()
            messages.success(request, "added to Saved blogs",'alert-success')
       else:
           bookmark.delete()
           messages.warning(request, "removed Saved blog",'alert-warning')
     
    except Exception as e:
        print(e)


    return redirect("blogs:blog_details_view",blog_id=blog_id) 



def update_challenge_view(request:HttpRequest):
    try:   
        if not request.user.is_superuser and not request.user.has_perm("blogs.change_challengequestion"):
            messages.warning(request,"You don't have permission to edit challenge","alert-warning")
            return redirect("main:home_view")
 
        challenge_question=ChallengeQuestion.objects.first()
        if request.method=="POST":
            challenge_question_form=ChallengeQuestionForm(request.POST,instance=challenge_question)
            if challenge_question_form.is_valid():
                challenge_question_form.save()
               
                messages.success(request, 'The challenge question has been updated successfully!','alert-success')
                return redirect("blogs:update_challenge_view")
            else:
                print("form is not valid")
                print(challenge_question_form.errors)
        else:   
            challenge_question_form = ChallengeQuestionForm(instance=challenge_question)        
        return render(request,'blogs/update_challenge.html',{"challenge_question":challenge_question})
    except ChallengeQuestion.DoesNotExist:
        print("error massege")
        messages.error(request, "An error occurred: The page not found",'alert-danger')
        return redirect('main:home_view')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('main:home_view')
