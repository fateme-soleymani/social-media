from django.urls import path

from apps.user.views import *

urlpatterns = [
    path('', FriendsPost.as_view(), name='friends_post'),
    # path('follow/<int:pk>/', UserFollow.as_view(), name='user_follow'),
    path('followers/', Follower.as_view(), name='followers'),
    path('following/', Following.as_view(), name='following'),
    path('edit_user/<int:pk>/', UpdateUser.as_view(), name='edit_user'),
    path('follow_requests/', FollowRequest.as_view(), name='follow_requests'),
    path('accept_requests/<int:pk>/', AcceptRequest.as_view(), name='accept'),
    path('delete_requests/<int:pk>/', DeleteRequest.as_view(), name='delete'),
    path('<slug:slug>/', UserDetail.as_view(), name='user_detail'),

    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate')
]
