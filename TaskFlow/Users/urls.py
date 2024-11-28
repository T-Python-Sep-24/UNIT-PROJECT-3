from django.urls import path
from . import views
from .views import RoleListView, AssignRoleView
from django.conf import settings
from django.conf.urls.static import static

app_name = "Users"

urlpatterns = [
    path('signup/', views.sign_up, name="sign_up"),
    path('signin/', views.sign_in, name="sign_in"),
    path('logout/', views.log_out, name="log_out"),
    path('profile/update/', views.update_user_profile, name="update_user_profile"),
    path('profile/<user_name>/', views.user_profile_view, name="user_profile_view"), 
    path('api/roles/', RoleListView.as_view(), name='role-list'),  # Fetch roles
    path('api/profiles/<int:profile_id>/assign-role/', AssignRoleView.as_view(), name='assign-role'),  # Assign role
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)