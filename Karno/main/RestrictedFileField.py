from django import forms
from django.db.models import FileField
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


class RestrictedFileField(FileField):
    """
    A FileField that allows only files with max size 20MB
    Author: Rana El-Garem
    """
    max_upload_size = 20971520  # 20 MB

    def clean(self, *args, **kwargs):
        data = super(RestrictedFileField, self).clean(*args, **kwargs)
        try:
            if data.size > self.max_upload_size:
                raise forms.ValidationError(
                    _('File size must be under %s. Current file size is %s.')
                    % (
                        filesizeformat(self.max_upload_size),
                        filesizeformat(data.size)))
        except AttributeError:
            pass
        return data
