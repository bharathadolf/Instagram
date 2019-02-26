from django import forms
from .models import Posts


class PostForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'id': 'customImage'}))
    class Meta:
        model = Posts
        fields = ['image', 'status']
