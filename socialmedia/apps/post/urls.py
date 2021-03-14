from django.urls import path

from apps.post.views import *

urlpatterns = [
               path('detail/<int:pk>', PostDetail.as_view(), name='post_detail'),
               path('create_post/', CreatePost.as_view(), name='create_post'),
               path('like/<int:pk>', LikePost.as_view(), name='like'),
               path('edit_post/<int:pk>', UpdatePost.as_view(), name='edit_post'),
               path('delete_post/<int:pk>', DeletePost.as_view(), name='delete_post'),
               path('delete_comment/<int:pk>', DeleteComment.as_view(), name='delete_cm'),
               ]
