from django import forms
from django.contrib.auth.forms import UserCreationForm

from board.models import User


class UserRegisterForm(UserCreationForm):
    avatar = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ('username', 'avatar', 'password1', 'password2')