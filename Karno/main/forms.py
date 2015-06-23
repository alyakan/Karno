from django import forms
from main.models import File, AudioFile, Tag, TempFile, ProfileImage
from main.models import YoutubeUrl
from django_select2.fields import AutoModelSelect2TagField


class YoutubeUrlForm(forms.ModelForm):
    url = forms.URLField(label='Youtube URL', required=True)

    class Meta:
        model = YoutubeUrl
        fields = ['url', ]


class TagField(AutoModelSelect2TagField):
    queryset = Tag.objects.all()
    choices = Tag.objects.all()
    search_fields = ['tag__icontains']

    def get_model_field_values(self, value):
        return {'tag': value}


class FileUploadForm(forms.ModelForm):
    file_uploaded = forms.FileField(label='Select a file')
    tags = TagField(required=False)

    class Meta:
        model = File
        fields = ['file_uploaded', 'user', 'public',
                  'registered_users', 'group', 'tags', 'tempId']


class AudioFileUploadForm(forms.ModelForm):
    title = forms.CharField(required=True)
    artist = forms.CharField(required=False)
    genre = forms.CharField(required=False)

    class Meta:
        model = AudioFile
        exclude = ['source_file', ]


class TempFileForm(forms.ModelForm):
    file_uploaded = forms.FileField(label='Select a file')

    class Meta:
        model = TempFile
        fields = ['file_uploaded', ]


class ProfileImageForm(forms.ModelForm):
    file_uploaded = forms.ImageField(label='Select a profile image')

    class Meta:
        model = ProfileImage
        fields = ['file_uploaded', 'user', 'tempId']
