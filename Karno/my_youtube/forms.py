from django import forms
from my_youtube.models import UploadedVideo


class YoutubeUploadForm(forms.Form):
    token = forms.CharField()
    file = forms.FileField()


class YoutubeDirectUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedVideo
        exclude = ('',)
