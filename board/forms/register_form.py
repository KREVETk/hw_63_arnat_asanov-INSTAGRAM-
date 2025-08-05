from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    phone_number = forms.CharField(required=False)
    gender = forms.ChoiceField(
        choices=User._meta.get_field('gender').choices,
        required=False
    )
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'avatar', 'first_name',
            'bio', 'phone_number', 'gender', 'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            existing_classes = widget.attrs.get('class', '')
            widget.attrs['class'] = f'{existing_classes} form-control'.strip()
