from django.urls import path, include

from apps.user.views import *

urlpatterns = [
    path('register/', AddUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('search/', Search.as_view(), name='search'),
    path('posts/',
         include([path('list/', PostList.as_view(), name='post_list'), path('detail/<int:pk>', PostDetail.as_view(), name='post_detail'),
                  ]), ),
]
