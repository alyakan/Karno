from django.db import models
from main.RestrictedFileField import RestrictedFileField
from django.contrib.auth.models import User
from datetime import datetime
from django.core.urlresolvers import reverse


class File(models.Model):

    """
    A Single File Entry
    Author: Rana El-Garem
    """
    file_uploaded = RestrictedFileField(upload_to='%Y/%m/%d')
    user = models.ForeignKey(User, related_name="file")
    public = models.BooleanField(default=False)
    registered_users = models.BooleanField(default=False)
    group = models.BooleanField(default=False)

    def extension(self):
        """
        Returns extension of file_uploaded
        Author: Rana El-Garem
        """
        name, extension = self.file_uploaded.name.split(".")
        return extension


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


class Comment(models.Model):
    """
    A Single Comment Entry
    Author: Nourhan Fawzy
    """
    description = models.CharField(max_length=512)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User, related_name="comment")
    file_uploaded = models.ForeignKey(File)

    def __unicode__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('comment-list', kwargs={'pk': self.pk})


class CommentNotification(models.Model):
    """
    Represents a notification when a user makes a comment on a file I shared
    Author: Nourhan Fawzy
    """
    comment = models.ForeignKey(Comment)
    file_shared = models.ForeignKey(File, null=False)   # file I shared
    user_notified = models.ForeignKey(User, null=False)
    # user_commented = models.ForeignKey(User, null=False)
    status = models.BooleanField(default=0)    # 0 means unread, 1 means read

    def __unicode__(self):
        return unicode(self.status)
