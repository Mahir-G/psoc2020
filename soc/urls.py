"""soc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

import projects.views as project_views
import mentors.views as mentor_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', project_views.Main.as_view(), name='main_page'),
    path('login/', mentor_views.Login.as_view(), name='user_login'),
    path('logout/', mentor_views.LogOut.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('mentors/', include('mentors.urls')),
    path('projects/', include('projects.urls')),
    path('mentees/', include('mentees.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)