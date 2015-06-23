from django.db import models
from main.RestrictedFileField import RestrictedFileField
from django.contrib.auth.models import User
import os
from Karno import settings
from datetime import datetime
from django.core.urlresolvers import reverse


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
    user = models.ForeignKey(User, related_name="file")
    public = models.BooleanField(default=False)
    registered_users = models.BooleanField(default=False)
    group = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    likes_count = models.IntegerField(default=0)
    tempId = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file_uploaded.name))
        super(File, self).delete(*args, **kwargs)

    def extension(self):
        """
        Returns extension of file_uploaded
        Author: Rana El-Garem
        """
        name, extension = self.file_uploaded.name.split(".")
        return extension

    def type(self):
        """
        Returns type of file_uploaded
        Author: Rana El-Garem
        """
        if (self.extension() == "png" or
                self.extension() == "jpeg" or self.extension() == "jpg"
                or self.extension() == "bmp"):
            return 'Image'
        elif (self.extension() == "mp4" or
                self.extension() == "mov"):
            return 'Video'
        elif (self.extension() == "mp3"
              or self.extension() == "ogg"
              or self.extension() == "wav"):
            return 'Audio'
        elif (self.extension() == "pdf"):
            return 'Document'
        else:
            return 'File'

    def privacy(self):
        """
        Returns level of privacy of File
        Author: Rana El-Garem
        """
        if self.public:
            return "Public"
        elif self.registered_users:
            return "Registered Users"
        elif self.group:
            return "Group"
        else:
            return "Only You"

    def group_users(self):
        """
        Returns list of users that have permission to view the File
        Author: Rana El-Garem
        """
        users = []
        groups = GroupPermission.objects.filter(file_uploaded=self)
        for group in groups:
            User.objects.get(id=group.user.id).username
            users.append(User.objects.get(id=group.user.id))
        return users


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


class Like(models.Model):

    """
    Represents a single Like on a file

    Author: Aly Yakan

    """
    user = models.ForeignKey(User)
    source_file = models.ForeignKey(File)


class TempFile(models.Model):
    """
    A TempFile created when an image is being uploaded for preview
    Author: Rana El-Garem
    """
    file_uploaded = RestrictedFileField(upload_to='temp/')
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file_uploaded.name))
        super(TempFile, self).delete(*args, **kwargs)


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


class ProfileImage(models.Model):
    """
    A single ProfileImage Entry belonging to a certain User
    Author: Rana El-Garem
    """

    file_uploaded = models.ImageField(upload_to='profile/', null=True)
    user = models.ForeignKey(User)
    tempId = models.IntegerField(default=0)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file_uploaded.name))
        super(ProfileImage, self).delete(*args, **kwargs)


class Notification(models.Model):
    """
    Notification for A user
    Author: Moustafa
    """
    message = models.CharField(max_length=128)
    file_shared = models.ForeignKey(File)
    user_notified = models.ForeignKey(User)
    status = models.BooleanField(default=0)
