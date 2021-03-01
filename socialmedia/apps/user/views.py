from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from apps.post.models import Post
from apps.user.forms import AddUserForm, LoginForm
from apps.user.models.user import User


# view for user register
class AddUser(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'user/user_form.html', {'form': form})

    def post(self, request):
        """
        save valid data in database(user)
        """
        form = AddUserForm(request.POST)
        if form.is_valid():
            validated_data = form.cleaned_data
            hash_pass = validated_data['password']
            first_name = validated_data['first_name']
            last_name = validated_data['last_name']
            date_of_birth = validated_data['date_of_birth']
            user_obj = User(user_name=validated_data['email'], first_name=first_name, last_name=last_name,
                            date_of_birth=date_of_birth, hash_pass=hash_pass)
            user_obj.save()
            # return redirect('ok')
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
            return render(request, 'user/my_profile.html', {'user': user})
        return render(request, 'user/login_form.html', {'form': form})


# view for search for username
class Search(View):
    def get(self, request):
        email = request.GET.get('email')
        if email:
            user = User.objects.filter(user_name__startswith=email)
        else:
            user = None
        return render(request, 'user/search.html', {'user': user})


class UserList(ListView):
    model = User
    context_object_name = 'list_user'


class UserDetail(DetailView):
    model = User
    context_object_name = 'profile_user'


class UserFollow(View):
    def get(self, request, pk):
        user = User.objects.get(first_name='ali')
        user.friends.add(User.objects.get(id=pk))
        ###
        return render(request, 'user/user_list.html')


class FriendsPost(View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        all_friends_posts = []
        for i in user.friends.all():
            all_friends_posts.append(Post.objects.filter(user=i))
        return render(request, 'post/friends_post_list.html', {'all_friends_posts': all_friends_posts})


class LogoutUser(View):
    def get(self, request):
        user = User.objects.get(login_status=True)
        user.login_status = False
        user.save()
        return redirect('index')
