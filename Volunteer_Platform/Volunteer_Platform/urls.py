from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Include main app URLs
    path('users/', include('users.urls')),
    path('opportunities/', include('opportunities.urls')),
    path('messaging/', include('messaging.urls')),
    path('reviews/', include('reviews.urls')),
]
