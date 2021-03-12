from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import View

from apps.post.models import Post
from apps.user.forms import RegisterUserForm
from apps.user.models.user import User, FollowerFollowing


# view for user register
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    success_url = '/login/'
    template_name = 'registration/register_user.html'

    def post(self, request):
        messages.success(request, 'User was successfully created.')
        return super(RegisterUser, self).post(request)


# view for search for username
class Search(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email')
        if email:
            user = User.objects.exclude(id=request.user.id).filter(email__startswith=email)
        else:
            user = None
        return render(request, 'user/search.html', {'user': user})


# show list of user
class UserList(LoginRequiredMixin, View):
    def get(self, request):
        user_friends = request.user.friends.all()
        user_except_you = User.objects.exclude(id=request.user.id)
        user_list = set(user_except_you) - set(user_friends)
        return render(request, 'user/user_list.html', {'user_list': user_list})


# view for show user profile
class UserDetail(LoginRequiredMixin, View):
    def get(self, request, slug):
        posts = Post.objects.filter(user__slug=slug)
        return render(request, 'user/user_profile.html', {'posts': posts})


# view for follow request
class UserFollow(LoginRequiredMixin, View):
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
        all_friends_posts = [Post.objects.filter(user=request.user)]
        following = FollowerFollowing.objects.filter(from_user=user, accept=True)
        for friend in following:
            all_friends_posts.append(Post.objects.filter(user=friend.to_user))
        return render(request, 'post/home_post.html', {'all_friends_posts': all_friends_posts})


# view for show followings
class Following(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        following = FollowerFollowing.objects.filter(from_user=user, accept=True)
        return render(request, 'user/following_list.html', {'following': following})


# view for show followers
class Follower(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        followers = FollowerFollowing.objects.filter(to_user=user, accept=True)
        return render(request, 'user/follower_list.html', {'followers': followers})


# view for edit user info
class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/edit_user.html'
    fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'link', 'bio']
    success_url = '/user/'


# view for follow request
class FollowRequest(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        follow_request = FollowerFollowing.objects.filter(to_user=user, accept=False)
        return render(request, 'user/follow_request.html', {'follow_request': follow_request})


# view for accept request
class AcceptRequest(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = request.user
        FollowerFollowing.objects.filter(to_user_id=user, from_user=pk).update(accept=True)
        return redirect('follow_requests')


# view for changing password
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


# view for login
class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        message = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_logout = request.POST.get("logout")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    message = 'Login was successful!'
                    login(request, user)
                    return redirect('friends_post')
                else:
                    message = 'User is deactivated!'
            else:
                message = 'Username or password was wrong!'
        elif is_logout:
            logout(request)
            message = 'Logout successful'
        return render(request, 'user/login.html', {'message': message})
