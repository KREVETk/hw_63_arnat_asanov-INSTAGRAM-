from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин или Email')
    password = forms.CharField(widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username_or_email and password:
            try:
                user = User.objects.get(email=username_or_email)
                username = user.username
            except User.DoesNotExist:
                username = username_or_email

            self.user = authenticate(username=username, password=password)

            if self.user is None:
                raise forms.ValidationError("Неверный логин/email или пароль")

        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)

    def get_next_url(self):
        return self.cleaned_data.get('next')
