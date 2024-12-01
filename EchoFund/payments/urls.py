from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('wallet/<wallet_id>/details', views.wallet_details, name='wallet_details'),
    path('wallet//add', views.add_wallet, name='add_wallet'),
    path('wallet/<wallet_id>/remove', views.delete_wallet, name='delete_wallet'),
    path('wallet/<wallet_id>/update', views.update_wallet, name='update_wallet'),
]