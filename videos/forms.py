from .models import Video
from django import forms

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'description', 'language', 'category', 'thumbnail', 'video')