from django import forms
from ..models import Comment


class CommentForm(forms.ModelForm):
    next = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Добавьте комментарий...',
                'class': 'form-control'
            }),
        }
