from django.urls import path
from .import views


app_name = "opportunities"

urlpatterns = [
    path("all/", views.all_opportunities_view, name="all_opportunities_view"),
    path('opportunity/<int:opportunity_id>/', views.opportunity_detail_view, name='opportunity_detail_view'),
    path("update-opportunity/<int:opportunity_id>/", views.update_opportunity_view, name="update_opportunity_view"),
    path("delete-opportunity/<int:opportunity_id>/", views.delete_opportunity_view, name="delete_opportunity_view"),
    path("apply/<int:opportunity_id>/", views.apply_to_opportunity_view, name="apply_to_opportunity_view"),
    path("opportunity/<int:opportunity_id>/apply/", views.update_opportunity_view, name="update_opportunity_view"),



]