from django.urls import path, include

from apps.user.views import *

urlpatterns = [
    path('register/', AddUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('search/', Search.as_view(), name='search'),
    path('list/', UserList.as_view(), name='user_list'),
    path('list/<int:pk>/', UserDetail.as_view(), name='user_detail'),
]
