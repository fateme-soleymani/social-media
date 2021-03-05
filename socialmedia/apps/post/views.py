from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.base import View

from apps.post.forms import CreatePostForm, CommentLike
from apps.post.models import Post, Comment, Like
from apps.user.models import User


# view for choose posts of user and send template
class PostList(View):
    def get(self, request):
        my_post_list = Post.objects.filter(user__login_status=True)
        return render(request, 'post/post_list.html', {'my_post_list': my_post_list})


# view for detail of post
class PostDetail(DetailView):
    model = Post
    context_object_name = 'my_post_detail'


# view for form create post
class CreatePost(View):
    def get(self, request):
        """
        send form(created post) to temp
        :param pk: user id
        """
        form = CreatePostForm()
        return render(request, 'post/post_create.html', {'form': form})

    def post(self, request):
        """
        save form data in database
        :param pk: user id
        """
        form = CreatePostForm(request.POST)
        if form.is_valid():
            user = User.objects.get(login_status=True)
            validated_data = form.cleaned_data
            user_obj = Post(title=validated_data['title'],
                            content=validated_data['content'], user=user)
            user_obj.save()
            # return redirect('ok')
        return render(request, 'post/post_create.html', {'form': form})


class CommentLikePost(View):
    def get(self, request):
        form = CommentLike()
        return render(request, 'post/post_detail.html', {'form': form})

    def post(self, request, pk):
        form = CommentLike(request.POST)
        if form.is_valid():
            validated_data = form.cleaned_data
            user = User.objects.get(login_status=True)
            comment_obj = Comment(text=validated_data['comment'], user=user, post_id=pk)
            comment_obj.save()
            message = 'your comment is added'
            # like_obj = Like(user=user, post_id=pk)
            # like_obj.save()
            return render(request, 'post/post_detail.html', {'form': form, 'message': message})
        return render(request, 'post/post_detail.html', {'form': form})
