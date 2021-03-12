from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views.generic.base import View

from apps.post.forms import CreatePostForm, CommentForm
from apps.post.models import Post, Comment, Like
from apps.user.models import User


# view for choose posts of user and send template
class PostList(LoginRequiredMixin, View):
    def get(self, request):
        my_post_list = Post.objects.filter(user=request.user)
        return render(request, 'post/post_list.html', {'my_post_list': my_post_list})


# view for detail of post
class PostDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        """
        :param pk: post id
        :return: form for comment and object of post
        """
        form = CommentForm()
        post = Post.objects.get(id=pk)
        my_comment = Comment.objects.filter(post=pk)
        return render(request, 'post/post_detail.html', {'form': form, 'post': post, 'my_comment': my_comment})

    def post(self, request, pk):
        """
        :param pk: post id
        save comment
        """
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            validated_data = form.cleaned_data
            comment_obj = Comment(text=validated_data['comment'], user=user, post_id=pk)
            comment_obj.save()
        return redirect('post_detail', pk)


# view for form create post
class CreatePost(LoginRequiredMixin, View):
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
            user = request.user
            validated_data = form.cleaned_data
            user_obj = Post(title=validated_data['title'],
                            content=validated_data['content'], user=user)
            user_obj.save()
        return render(request, 'post/post_create.html', {'form': form})

# view for liking a post
class LikePost(LoginRequiredMixin, View):
    def get(self, request, pk):
        """
        :param pk: post id
        save like
        """
        user = request.user
        like_obj = Like(user=user, post_id=pk)
        if Like.objects.filter(user=user, post_id=pk):
            pass
        else:
            like_obj.save()
        return redirect('post_detail', pk)

# view for editing a post
class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post/edit_post.html'
    fields = ['title', 'content']
    success_url = '/user/'

# view for deleting a post
class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/user/'

# view for editing a comment
class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = '/user/'
