from . import views
from django.urls import path

app_name="partners"

urlpatterns=[
    path("new/request/<sender_id>/<recevier_id>/",views.new_request_view,name="new_request_view"),
    path("delete/request/<sender_id>/<recevier_id>/",views.delete_request_view,name="delete_request_view"),
    path("new/partner/<user_id>/<partner_id>/",views.new_partner_view,name="new_partner_view"),
    path("delete/partner/<user_id>/<partner_id>/",views.delete_partner_view,name="delete_partner_view"),
    path("edit/schedule/<user_id>/<partner_id>/",views.edit_schedule_view,name="edit_schedule_view"),
    path("new/message/<sender_id>/<recevier_id>/",views.new_message_view,name="new_message_view"),
    path("delete/message/<message_id>/",views.delete_message_view,name="delete_message_view"),
    path('mark_messages_as_read/', views.mark_messages_as_read, name='mark_messages_as_read'),
    path("start/chat/room/",views.start_chat_room,name="start_chat_room"),
    path('get_token/', views.getToken),
    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
    
]