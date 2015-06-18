from django import forms
from main.models import File


class FileUploadForm(forms.ModelForm):
    file_uploaded = forms.FileField(label='Select a file')

    class Meta:
        model = File
        fields = ['file_uploaded', 'user',
                  'public', 'registered_users', 'group']
