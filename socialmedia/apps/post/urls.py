from django.urls import path, include

from apps.post.views import *

urlpatterns = [
    path('my_profile/',
         include([path('<int:pk>/', PostList.as_view(), name='post_list'),
                  path('detail/<int:pk>', PostDetail.as_view(), name='post_detail'),
                  path('<int:pk>/create_post', CreatePost.as_view(), name='create_post'),
                  ]), ),
]
