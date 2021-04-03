from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView
from django.views.generic.base import View
from django.contrib import messages

from apps.post.forms import *
from apps.post.models import Post, Comment


# view for detail of post
class PostDetail(View):
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
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            validated_data = form.cleaned_data
            post_obj = Post(title=validated_data['title'],
                            content=validated_data['content'], post_pic=validated_data['post_pic'], user=user)
            post_obj.save()
            messages.success(request, 'Post created successfully')
        return redirect('friends_post')


class LikePost(View):
    def get(self, request, pk):
        """
        :param pk: post id
        save like
        """
        user = request.user
        post = Post.objects.get(id=pk)
        post.like.add(user)
        return redirect('friends_post')


class UpdatePost(UpdateView):
    model = Post
    template_name = 'post/edit_post.html'
    fields = ['title', 'content', 'post_pic']
    success_url = '/user/'


class DeletePost(DeleteView):
    model = Post
    success_url = '/user/'


class DeleteComment(DeleteView):
    model = Comment
    success_url = '/user/'
