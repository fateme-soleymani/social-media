from django import forms


# form for create post
class CreatePostForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)


class CommentLike(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    like = forms.BooleanField()
