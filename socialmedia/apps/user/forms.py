import hashlib
from django import forms
from apps.user.models.user import User


# form for register
class RegisterUserForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(required=False)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', max_length=20)
    re_password = forms.CharField(label='Re_password', max_length=20)

    def clean(self):
        """
        check validation for form field
        :return:Appropriate error or cleaned data
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        if len(password) < 5:
            raise forms.ValidationError('Password must be at least 5 characters')
        if User.objects.filter(user_name=email).exists():
            raise forms.ValidationError('Email addresses must be unique')
        if not password == re_password:
            raise forms.ValidationError('Passwords must match')
        return cleaned_data


# form for user login
class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=200)
    password = forms.CharField(max_length=30)

    def clean(self):
        """
        Check user registration and password authentication
        :return:Appropriate error or cleaned data
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('user_name')
        password = cleaned_data.get('password')
        password2 = hashlib.sha256(str(password).encode()).hexdigest()
        if User.objects.filter(login_status=True):
            raise forms.ValidationError("sorry other user is login!")
        else:
            if not User.objects.filter(user_name=email).exists():
                raise forms.ValidationError("this username doesn't exist")
            else:
                if not User.objects.filter(user_name=email, hash_pass=password2).exists():
                    raise forms.ValidationError("pass wrong")
                else:
                    return cleaned_data
