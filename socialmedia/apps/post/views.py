from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.base import View

from apps.post.models import Post


class PostList(View):
    def get(self, request, pk):
        my_post_list = Post.objects.filter(user_id=pk)
        return render(request, 'post/post_list.html', {'my_post_list': my_post_list})


class PostDetail(DetailView):
    model = Post
    context_object_name = 'my_post_detail'
