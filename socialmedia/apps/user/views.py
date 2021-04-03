from random import randint

import ghasedak
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import View

from apps.post.models import Post
from apps.user.forms import RegisterUserForm, SmsForm
from apps.user.models.followerfollowing import FollowerFollowing
from apps.user.models.user import User
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

                if form.cleaned_data['phone'] == None:
                    user.username = form.cleaned_data['email']
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
                    email_body = 'Hi please use this link to verify your account\n\n' + activate_url
                    email_subject = 'Activate your account'
                    email = form.cleaned_data.get('email')
                    email = EmailMessage(
                        email_subject, email_body, to=[email]
                    )
                    email.send()
                    return HttpResponse('Please confirm your email address to complete the registration')

                else:
                    user.username = form.cleaned_data['phone']
                    token = randint(100, 999)
                    user.sms_verify = token
                    user.save()
                    sms = ghasedak.Ghasedak("")
                    sms.send({'message': "Use " + str(token) + " to verify your account.",
                              'receptor': form.cleaned_data['phone'],
                              'linenumber': "10008566"})
                    return redirect('sms', pk=user.id)
            else:
                message = 'You must enter a valid email or phone number!'
                return render(request, 'registration/register_user.html', {'form': form, 'message': message})
        else:
            form = RegisterUserForm()
            return render(request, 'registration/register_user.html', {'form': form})


class SmsView(View):
    def get(self, request, pk):
        form = SmsForm()
        return render(request, 'registration/smsverify.html', {'form': form})

    def post(self, request, pk):
        form = SmsForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=pk)
            validated_data = form.cleaned_data
            if validated_data['sms'] == user.sms_verify:
                user.is_active = True
                user.save()
                return redirect('/')
            else:
                message = 'The code you enter is incorrect!'
                return render(request, 'registration/smsverify.html', {'form': form, 'message': message})

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
        user = User.objects.get(slug=slug)
        flag = False
        if user.id == request.user.id or FollowerFollowing.objects.filter(from_user=request.user, to_user=user,
                                                                          accept=True):
            flag = True
        return render(request, 'user/user_profile.html', {'posts': posts, 'user': user, 'flag': flag})


# view for follow request
class UserFollow(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = request.user
        user.friends.add(User.objects.get(id=pk))
        return redirect('friends_post')


# view for  show following post in home
class FriendsPost(LoginRequiredMixin, View):
    def get(self, request):
        following_id = [request.user.id]
        posts = []
        for obj in FollowerFollowing.objects.filter(from_user=request.user, accept=True):
            following_id.append(obj.to_user.id)
        following = User.objects.filter(id__in=following_id)
        for post in Post.objects.all():
            if post.user in following:
                posts.append(post)
        return render(request, 'post/home_post.html', {'posts': posts})


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
class UpdateUser(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'user/edit_user.html'
    fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'phone', 'link', 'bio', 'profile_pic']

    success_message = 'Your information has been updated'
    success_url = '/user/'


# view for follow request
class FollowRequest(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        follow_request = FollowerFollowing.objects.filter(to_user=user, accept=False)
        follow_request_list = list(follow_request)
        if len(follow_request_list) == 0:
            follow_request = 0
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
                    login(request, user)
                    messages.success(request, 'Login was successful!')
                    return redirect('friends_post')
                else:
                    message = 'User is deactivated!'
            else:
                message = 'Username or password was wrong!'
        elif is_logout:
            logout(request)
            message = 'Logout successful'

        return render(request, 'user/login.html', {'message': message})
