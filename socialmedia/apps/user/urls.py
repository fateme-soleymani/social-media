from django.urls import path

from apps.user.views import *

urlpatterns = [
    path('', FriendsPost.as_view(), name='friends_post'),
    path('search/', Search.as_view(), name='search'),
    path('list/', UserList.as_view(), name='user_list'),
    path('list/<slug:slug>/', UserDetail.as_view(), name='user_detail'),
    path('follow/<int:pk>/', UserFollow.as_view(), name='user_follow'),
    path('followers/', Follower.as_view(), name='followers'),
    path('following/', Following.as_view(), name='following'),
    path('edit_user/<int:pk>/', UpdateUser.as_view(), name='edit_user'),
    path('follow_requests/', FollowRequest.as_view(), name='follow_requests'),
    path('accept_requests/<int:pk>/', AcceptRequest.as_view(), name='accept'),

]
