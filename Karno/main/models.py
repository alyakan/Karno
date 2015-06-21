from django.db import models
from main.RestrictedFileField import RestrictedFileField
from django.contrib.auth.models import User
import os
from Karno import settings


class Tag(models.Model):
    """
    A Single Tag Entry
    Author: Rana El-Garem
    """
    tag = models.CharField(max_length=15, unique=True)

    def __unicode__(self):
        return unicode(self.tag)


class File(models.Model):

    """
    A Single File Entry
    Author: Rana El-Garem
    """
    file_uploaded = RestrictedFileField(upload_to='%Y/%m/%d')
    user = models.ForeignKey(User)
    public = models.BooleanField(default=False)
    registered_users = models.BooleanField(default=False)
    group = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    tempId = models.IntegerField()

    def extension(self):
        """
        Returns extension of file_uploaded
        Author: Rana El-Garem
        """
        name, extension = self.file_uploaded.name.split(".")
        return extension


class AudioFile(models.Model):
    title = models.CharField(max_length=32)
    artist = models.CharField(max_length=12)
    genre = models.CharField(max_length=12)
    source_file = models.ForeignKey(File)


class GroupPermission(models.Model):

    """
    A Single GroupPermission
    Entry Author: Rana El-Garem
    """
    file_uploaded = models.ForeignKey(File)
    user = models.ForeignKey(User)


class YoutubeUrl(models.Model):
    """
    Represents a single existing Youtube Url to be embeded

    Author: Aly Yakan

    """
    url = models.CharField(max_length=128, null=False)
    video_id = models.CharField(max_length=128)
    user = models.ForeignKey(User)


class TempFile(models.Model):
    file_uploaded = RestrictedFileField(upload_to='temp/')
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file_uploaded.name))
        super(TempFile, self).delete(*args, **kwargs)
