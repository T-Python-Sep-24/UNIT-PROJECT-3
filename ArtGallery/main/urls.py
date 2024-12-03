from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.homeView, name='homeView'),
    path("contact/", views.contactView, name="contactView"),
    path("contact/messages", views.allMessagesView, name="allMessagesView"),
    path("contact/messages/delete/<int:msgId>", views.deleteMessageView, name="deleteMessageView"),

]