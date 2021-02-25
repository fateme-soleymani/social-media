from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.base import View

from apps.post.forms import CreatePostForm
from apps.post.models import Post
from apps.user.models import User


class PostList(View):
    def get(self, request, pk):
        my_post_list = Post.objects.filter(user_id=pk)
        return render(request, 'post/post_list.html', {'my_post_list': my_post_list})


class PostDetail(DetailView):
    model = Post
    context_object_name = 'my_post_detail'


class CreatePost(View):
    def get(self, request, pk):
        form = CreatePostForm()
        return render(request, 'post/post_create.html', {'form': form})

    def post(self, request, pk):
        form = CreatePostForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=pk)
            validated_data = form.cleaned_data
            user_obj = Post(title=validated_data['title'],
                            content=validated_data['content'], user=user)
            user_obj.save()
            # return redirect('ok')
        return render(request, 'post/post_create.html', {'form': form})
