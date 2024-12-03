from django.urls import path
from . import views

app_name = 'funds_app'

urlpatterns = [
    path('all/', views.all_funds_view, name='all_funds_view'),
    path('my/funds', views.user_funds_view, name='user_funds_view'),
    path('participated/in/', views.user_participated_in_funds_view, name='user_participated_in_funds_view'),
    path('details/<fund_id>', views.fund_details_view, name='fund_details_view'),
    path('add/', views.add_fund_view, name='add_fund_view'),
    path('update/<fund_id>', views.update_fund_view, name='update_fund_view'),
    path('delete/<fund_id>', views.delete_fund_view, name='delete_fund_view'),
    path('start/<fund_id>', views.start_fund, name='start_fund'),
    path('participate/<fund_id>', views.fund_participate_view, name='fund_participate_view'),
    # urls.py
    path('schedule/<fund_id>/', views.payment_schedule, name='payment_schedule'),

    path('review/add/<fund_id>', views.add_review_view, name='add_review_view'),
    path('review/delete/<review_id>', views.delete_review_view, name='delete_review_view'),

    path('bookmark/add/<fund_id>', views.add_bookmark_view, name='add_bookmark_view'),
]