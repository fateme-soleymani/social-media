from django.urls import path, include

from apps.post.views import *

urlpatterns = [path('my_post/', PostList.as_view(), name='my_post_list'),
               path('detail/<int:pk>', PostDetail.as_view(), name='post_detail'),
               path('create_post/', CreatePost.as_view(), name='create_post'),
               ]
