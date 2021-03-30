from django import forms

from django.forms import ModelForm

from apps.post.models import Post


# form for create post
class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_pic']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        post_pic = cleaned_data.get('post_pic')
        if content == '' and post_pic == None:
            raise forms.ValidationError('You must enter an image or content')
        else:
            return cleaned_data


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

# class UpdatePostForm(ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'post_pic']
#
#     def clean(self):
#         cleaned_data = super().clean()

