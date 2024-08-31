from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Profile


class RegisterForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")
