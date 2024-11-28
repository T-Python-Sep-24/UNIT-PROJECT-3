from django.urls import path
from . import views
app_name = "products"
urlpatterns = [

    path("all/", views.all_product,name="all_product"),
    path("add/", views.add_product,name="add_product"),
    path('detail/<product_id>/', views.detail_product,name='detail_product'),
    path("update/<product_id>", views.update_product,name="update_product"),
    path("delete/<product_id>", views.delete_product,name="delete_product"),

]