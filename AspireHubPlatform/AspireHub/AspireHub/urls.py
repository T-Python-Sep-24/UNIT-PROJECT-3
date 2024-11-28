"""
URL configuration for AspireHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/',include("main_app.urls")),
    path('career/',include("career_path_app.urls")),
    path('courses/',include("courses_certifications_app.urls")),
    path('companies/',include("events_companies_app.urls")),
    path('contact/',include("contact_app.urls")),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)




