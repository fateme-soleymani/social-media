import hashlib

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.base import View

from apps.post.models import Post
from apps.user.forms import RegisterUserForm, LoginForm
from apps.user.models.user import User


# view for user register
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    success_url = '/login/'
    template_name = 'registration/register_user.html'

    def post(self, request):
        messages.success(request, 'User was successfully created.')
        return super(RegisterUser, self).post(request)


# view for search for username
class Search(View):
    def get(self, request):
        email = request.GET.get('email')
        if email:
            user = User.objects.exclude(id=request.user.id).filter(email__startswith=email)
        else:
            user = None
        return render(request, 'user/search.html', {'user': user})


# show list of user
class UserList(View):
    def get(self, request):
        user_friends = request.user.friends.all()
        user_except_you = User.objects.exclude(id=request.user.id)
        user_list = set(user_except_you) - set(user_friends)
        return render(request, 'user/user_list.html', {'user_list': user_list})


# view for show user profile
class UserDetail(View):
    def get(self, request, pk):
        posts = Post.objects.filter(user_id=pk)
        return render(request, 'user/user_profile.html', {'posts': posts})


# view for follow request
class UserFollow(View):
    def get(self, request, pk):
        user = request.user
        user.friends.add(User.objects.get(id=pk))
        user_friends = User.objects.get(id=request.user.id).friends.all()
        user_except_you = User.objects.exclude(id=request.user.id)
        user_list = set(user_except_you) - set(user_friends)
        return render(request, 'user/user_list.html', {'user_list': user_list})


# view for  show following post in home
class FriendsPost(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        all_friends_posts = []
        for friend in user.friends.all():
            all_friends_posts.append(Post.objects.filter(user=friend))
        return render(request, 'post/home_post.html', {'all_friends_posts': all_friends_posts})


# view for logout
# class LogoutUser(View):
#     def get(self, request):
#         user = request.user
#         user.login_status = False
#         user.save()
#         return redirect('index')


# view for show followings
class Following(View):
    def get(self, request):
        user = request.user
        following = user.friends.all()
        return render(request, 'user/following_list.html', {'following': following})


# view for show followers
class Follower(View):
    def get(self, request):
        user = User.objects.all()
        followers = []
        for u in user:
            if u.friends.filter(id=request.user.id):
                followers.append(u)
        return render(request, 'user/follower_list.html', {'followers': followers})

class UpdateUser(UpdateView):
    model = User
    template_name = 'user/edit_user.html'
    fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'link', 'bio', 'password']
    success_url = '/user/'
