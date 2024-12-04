from django.urls import path
from . import views

app_name ="events_companies_app"

urlpatterns = [
    path("add/company/", views.add_company_view , name="add_company_view"),
    path("add/employee/", views.add_employee_view , name="add_employee_view"),
    path("add/event/", views.add_event_view , name="add_event_view"),
    path("lists/company/events/", views.lists_companies_events_view, name="lists_companies_events_view"),
    path("details/company/<company_id>", views.details_companies_view, name="details_companies_view"),
    path("details/events/<event_id>", views.details_events_view , name="details_events_view"),
    path("update/company/<company_id>", views.update_company_view , name="update_company_view"),
    path("update/employee/<employee_id>", views.update_employee_view , name="update_employee_view"),
    path("update/event/<event_id>", views.update_event_view , name="update_event_view"),
    path("delete/company/<company_id>", views.delete_company_view, name="delete_company_view"),
    path("delete/employee/<employee_id>", views.delete_employee_view, name="delete_employee_view"),
    path("delete/event/<event_id>", views.delete_event_view, name="delete_event_view"),
]