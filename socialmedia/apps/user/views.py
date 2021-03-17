from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import View

from apps.post.models import Post
from apps.user.forms import RegisterUserForm
from apps.user.models.user import User
from apps.user.models.followerfollowing import FollowerFollowing

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_genarator


# view for user register
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    success_url = '/'
    template_name = 'registration/register_user.html'

    def post(self, request):
        if request.method == 'POST':
            form = RegisterUserForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                """path to view
                    -getting domain we are on 
                    -relative url to verification
                    -encode uid
                    -token 
                      """
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                    'uidb64': uidb64, 'token': token_genarator.make_token(user)}
                               )
                activate_url = 'http://' + domain + link
                email_body = 'Hi' + user.email + 'please use this link to verify your account\n' + activate_url
                email_subject = 'Activate your account'
                email = form.cleaned_data.get('email')
                email = EmailMessage(
                    email_subject, email_body, to=[email]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = RegisterUserForm()
        return render(request, 'registration/register_user.html', {'form': form})


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and token_genarator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse('Activation link is invalid!')


# view for show user profile
class UserDetail(LoginRequiredMixin, View):
    def get(self, request, slug):
        posts = Post.objects.filter(user__slug=slug)
        return render(request, 'user/user_profile.html', {'posts': posts})


# # view for follow request
# class UserFollow(LoginRequiredMixin, View):
#     def get(self, request, pk):
#         user = request.user
#         user.friends.add(User.objects.get(id=pk))
#         user_friends = User.objects.get(id=request.user.id).friends.all()
#         user_except_you = User.objects.exclude(id=request.user.id)
#         user_list = set(user_except_you) - set(user_friends)
#         return render(request, 'user/user_list.html', {'user_list': user_list})


# view for  show following post in home
class FriendsPost(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        all_friends_posts = [Post.objects.filter(user=request.user)]
        following = FollowerFollowing.objects.filter(from_user=user, accept=True)
        for friend in following:
            all_friends_posts.append(Post.objects.filter(user=friend.to_user).order_by('created'))
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
        follower = FollowerFollowing.objects.filter(to_user=user, accept=True)
        return render(request, 'user/follower_list.html', {'follower': follower})


# view for edit user info
class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/edit_user.html'
    fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'link', 'bio', 'profile_pic']
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


# view for delete request
class DeleteRequest(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = request.user
        FollowerFollowing.objects.filter(to_user_id=user, from_user=pk).delete()
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
