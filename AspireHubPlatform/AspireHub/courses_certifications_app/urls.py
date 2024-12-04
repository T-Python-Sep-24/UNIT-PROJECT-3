from django.urls import path
from . import views

app_name ="courses_certifications_app"

urlpatterns = [
    path("add/course/", views.add_course_view , name="add_course_view"),
    path("add/certification/", views.add_certification_view , name="add_certification_view"),
    path("lists/courses/certifications/", views.lists_courses_certifications_view , name="lists_courses_certifications_view"),
    path("details/course/<course_id>", views.details_course_view, name="details_course_view"),
    path("details/certification/<certification_id>", views.details_certification_view , name="details_certification_view"),
    path("update/course/<course_id>", views.update_course_view , name="update_course_view"),
    path("update/certification/<certification_id>", views.update_certification_view , name="update_certification_view"),
    path("delete/course/<course_id>", views.delete_course_view, name="delete_course_view"),
    path("delete/certification/<certification_id>", views.delete_certification_view, name="delete_certification_view"),

]