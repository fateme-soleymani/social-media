"""socialmedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.views.generic import TemplateView

from apps.user import views
from apps.user.views import RegisterUser, LoginView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('user/', include('apps.user.urls')),
    path('post/', include('apps.post.urls'), name='posts'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('password/', views.change_password, name='change_password'),
]
