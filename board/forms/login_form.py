from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин или Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            user = authenticate(self.request, username=username_or_email, password=password)
            if user is None:
                UserModel = get_user_model()
                try:
                    user_obj = UserModel.objects.get(email=username_or_email)
                    user = authenticate(self.request, username=user_obj.username, password=password)
                except UserModel.DoesNotExist:
                    user = None

            if user is None:
                raise forms.ValidationError("Неверный логин/email или пароль.")
            else:
                self.confirm_login_allowed(user)
                self.user_cache = user

        return self.cleaned_data
