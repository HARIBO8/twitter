from django import forms
from .models import Profile, Tweet

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

