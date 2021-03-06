"""ghanaiem_agency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from os import name
from django.contrib import admin
from django.urls import path
from django.urls.conf import include, include
from main.views import index, terms, privacy, annonces_by_category
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('categories/', annonces_by_category, name='categories'),
    path('categorie/<rubrique_slug>/', annonces_by_category, name='categories'),
    path('term-of-use/', terms, name='terms'),
    path('privacy-poilcy/', privacy, name='privacy'),
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("app/", include("apps.home.urls", namespace='home')) # UI Kits Html files
]

 
urlpatterns += static(settings.MEDIA_URL, 
                        document_root=settings.MEDIA_ROOT) 
urlpatterns += static(settings.STATIC_URL, 
                              document_root=settings.STATIC_ROOT)