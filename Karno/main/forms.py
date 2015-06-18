from django import forms
from main.models import YoutubeUrl
from main.models import File


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
