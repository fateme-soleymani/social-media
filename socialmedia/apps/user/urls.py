from django.urls import path, include

from apps.user.views import *

urlpatterns = [
    path('register/', AddUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('search/', Search.as_view(), name='search'),
]
