from django.urls import path
from . import views
from .views import PredictView


app_name ="career_path_app"

urlpatterns = [
    # path("career/test/", views.career_test_view , name="career_test_view"),
    path('api/predict/', PredictView.as_view(), name='predict'),

]



