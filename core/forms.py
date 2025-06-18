from django import forms
from .models import Profile, Tweet

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']