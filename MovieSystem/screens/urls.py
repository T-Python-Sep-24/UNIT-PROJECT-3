from django.urls import path
from . import views



app_name='screens'

urlpatterns = [
   path('all/',views.all_screens_view,name='all_screens_view'),
   path('add/',views.add_screen_view,name='add_screen_view'),
   path('update/<screen_id>/',views.update_screen_view,name='update_screen_view'),
   path('delete/<screen_id>',views.delete_screen_view,name='delete_screen_view')
]