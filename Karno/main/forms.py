from django import forms
from main.models import YoutubeUrl


class YoutubeUrlForm(forms.ModelForm):
    url = forms.URLField(label='Youtube URL', required=True)

    class Meta:
        model = YoutubeUrl
        fields = ['url', ]
