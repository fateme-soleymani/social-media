from django.urls import path, include

from apps.user.views import *

urlpatterns = [
    path('search/', Search.as_view(), name='search'),
    path('list/', UserList.as_view(), name='user_list'),
    path('list/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('follow/<int:pk>/', UserFollow.as_view(), name='user_follow'),
    path('', FriendsPost.as_view(), name='friends_post'),
    path('followers/', Follower.as_view(), name='followers'),
    path('following/', Following.as_view(), name='following'),
    path('edit_user/<int:pk>/', UpdateUser.as_view(), name='edit_user'),
]
