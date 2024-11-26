from django.urls import path 
from . import views

app_name = "services"

urlpatterns = [
    path('products',views.products_view,name="products_view"),   
    path('products/add',views.add_product_view,name="add_product_view"),
    path('products/detail/<product_id>',views.product_detail_view,name="product_detail_view"),
    path('products/update',views.update_product_view,name="update_product_view"),
    path('products/delete/<product_id>',views.product_delete_view,name="product_delete_view"),
]