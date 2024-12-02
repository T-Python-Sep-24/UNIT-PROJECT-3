from django.urls import path
from . import views

app_name ="events_companies_app"

urlpatterns = [
    path("add/company/", views.add_company_view , name="add_company_view"),
    path("add/employee/", views.add_employee_view , name="add_employee_view"),
    path("add/event/", views.add_event_view , name="add_event_view"),
    path("lists/company/events/", views.lists_companies_events_view, name="lists_companies_events_view"),
    path("details/company/", views.details_companies_view, name="details_companies_view"),
    path("events/list/", views.events_list_view , name="events_list_view"),
    path("update/company/<int:company_id>", views.update_company_view , name="update_company_view"),
    path("update/employee/<int:employee_id>", views.update_employee_view , name="update_employee_view"),
    path("update/event/<int:event_id>", views.update_event_view , name="update_event_view"),
    path("delete/company/<int:company_id>", views.delete_company_view, name="delete_company_view"),
    path("delete/employee/<int:employee_id>", views.delete_employee_view, name="delete_employee_view"),
    path("delete/event/<int:event_id>", views.delete_event_view, name="delete_event_view"),
]