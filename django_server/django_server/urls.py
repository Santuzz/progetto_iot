"""
URL configuration for django_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from init_db import *

urlpatterns = [
    # Include URLs from the REST app under the 'api/' prefix
    path("admin/", admin.site.urls),
    path('api/', include('REST.urls')),
    path('api-auth/', include('rest_framework.urls'))

]

# inserire qui gli script utili per quando viene avviato il server

# erase_db()
# init_db()
