import hashlib

from django import forms

from apps.user.models.user import User
from common.validators import pass_valid


class AddUserForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(required=False)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', max_length=20, validators=[pass_valid])
    re_password = forms.CharField(label='Re_password', max_length=20, validators=[pass_valid])

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        if User.objects.filter(user_name=email).exists():
            raise forms.ValidationError('Email addresses must be unique')
        if not password == re_password:
            raise forms.ValidationError('Passwords must match')
        return cleaned_data


class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=200)
    password = forms.CharField(max_length=30)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('user_name')
        password = cleaned_data.get('password')
        password2 = hashlib.sha256(str(password).encode()).hexdigest()
        if not User.objects.filter(user_name=email).exists():
            raise forms.ValidationError("this username doesn't exist")
        else:
            if not User.objects.filter(user_name=email, hash_pass=password2).exists():
                raise forms.ValidationError("pass wrong")
            else:
                return cleaned_data
