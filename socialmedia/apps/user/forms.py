from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.user.models.user import User


# form for register
class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'profile_pic', 'email', 'phone', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        if email == None and phone == None:
            raise forms.ValidationError('You must enter an email or phone number')
        else:
            return cleaned_data
