from django.urls import path
from . import views
app_name = "products"
urlpatterns = [

    path("all/", views.all_product,name="all_product"),
    path("add/", views.add_product,name="add_product"),
    path('detail/<int:product_id>/', views.detail_product, name='detail_product'),
    path("<int:product_id>/add-review/", views.add_review_view, name="add_review"),
    path("review/<int:review_id>/delete/", views.delete_review_view, name="delete_review"),
    path("update/<product_id>", views.update_product,name="update_product"),
    path("delete/<product_id>", views.delete_product,name="delete_product"),

]