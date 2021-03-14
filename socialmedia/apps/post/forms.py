from django import forms

from django.forms import ModelForm

from apps.post.models import Post


# form for create post
class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_pic']


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
