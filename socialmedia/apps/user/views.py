import hashlib

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from apps.post.models import Post
from apps.user.forms import RegisterUserForm, LoginForm
from apps.user.models.user import User


# view for user register
class RegisterUser(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'user/user_form.html', {'form': form})

    def post(self, request):
        """
        save valid data in database(user)
        """
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            validated_data = form.cleaned_data
            hash_pass = hashlib.sha256(str(validated_data['password']).encode()).hexdigest()
            first_name = validated_data['first_name']
            last_name = validated_data['last_name']
            date_of_birth = validated_data['date_of_birth']
            user_obj = User(user_name=validated_data['email'], first_name=first_name, last_name=last_name,
                            date_of_birth=date_of_birth, hash_pass=hash_pass, login_status=True)
            user_obj.save()
            return redirect('friends_post')
        return render(request, 'user/user_form.html', {'form': form})


# view for user login
class LoginUser(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login_form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(user_name=form.cleaned_data['user_name'])
            user.login_status = True
            user.save()
            return redirect('friends_post')
        return render(request, 'user/login_form.html', {'form': form})


# view for search for username
class Search(View):
    def get(self, request):
        email = request.GET.get('email')
        if email:
            user = User.objects.filter(login_status=False, user_name__startswith=email)
        else:
            user = None
        return render(request, 'user/search.html', {'user': user})


class UserList(View):
    def get(self, request):
        user_list = User.objects.exclude(login_status=True)
        return render(request, 'user/user_list.html', {'user_list': user_list})


class UserDetail(DetailView):
    model = User
    context_object_name = 'profile_user'


class UserFollow(View):
    def get(self, request, pk):
        user = User.objects.get(login_status=True)
        user.friends.add(User.objects.get(id=pk))
        return render(request, 'user/user_list.html')


class FriendsPost(View):
    def get(self, request):
        user = User.objects.get(login_status=True)
        print(user)
        all_friends_posts = []
        print(user.friends.all())
        for friend in user.friends.all():
            all_friends_posts.append(Post.objects.filter(user=friend))
        print(all_friends_posts)
        return render(request, 'post/home_post.html', {'all_friends_posts': all_friends_posts})


class LogoutUser(View):
    def get(self, request):
        user = User.objects.get(login_status=True)
        user.login_status = False
        user.save()
        return redirect('index')
