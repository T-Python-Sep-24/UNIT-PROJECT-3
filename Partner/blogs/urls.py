from . import views
from django.urls import path

app_name="blogs"

urlpatterns=[
    path('all/',views.blogs_all_view,name="blogs_all_view"),
    path('add/',views.new_blog_view,name="new_blog_view"),
    path('update/<blog_id>',views.update_blog_view,name="update_blog_view"),
    path('delete/<blog_id>',views.delete_blog_view,name="delete_blog_view"),
    path('comment/add/<blog_id>',views.add_comment_view,name="add_comment_view"),
    path('comment/delete/<comment_id>',views.delete_comment_view,name="delete_comment_view"),
    path('details/<blog_id>/',views.blog_details_view,name="blog_details_view"),
    path('bookmarks/add/<blog_id>/',views.add_bookmark_view,name="add_bookmark_view"),

]