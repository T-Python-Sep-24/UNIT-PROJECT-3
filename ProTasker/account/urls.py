from django.urls import path
from . import views


app_name="account"

urlpatterns=[

    path("sign/up",views.sign_up,name="sign_up"),
    path("sign/in",views.sign_in,name="sign_in"),
     path("logout",views.log_out,name="log_out")
    
]