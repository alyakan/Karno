from django import forms
from main.models import File, AudioFile
from main.models import YoutubeUrl


class YoutubeUrlForm(forms.ModelForm):
    url = forms.URLField(label='Youtube URL', required=True)

    class Meta:
        model = YoutubeUrl
        fields = ['url', ]


class FileUploadForm(forms.ModelForm):
    file_uploaded = forms.FileField(label='Select a file')

    class Meta:
        model = File
        fields = ['file_uploaded', 'user',
                  'public', 'registered_users', 'group']


class AudioFileUploadForm(forms.ModelForm):
    title = forms.CharField(required=True)
    artist = forms.CharField(required=False)
    genre = forms.CharField(required=False)

    class Meta:
        model = AudioFile
        exclude = ['source_file', ]
