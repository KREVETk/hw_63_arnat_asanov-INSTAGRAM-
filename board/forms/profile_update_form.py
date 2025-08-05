from django import forms
from ..models import User


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'bio', 'phone_number', 'gender', 'email']


