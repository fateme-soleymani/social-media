from django.contrib.auth.forms import UserCreationForm
from apps.user.models.user import User


# form for register
class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('profile_pic','email', 'first_name', 'last_name', 'date_of_birth', 'password1', 'password2', 'link', 'gender', 'bio')
