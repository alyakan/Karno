from django.db import models
from main.RestrictedFileField import RestrictedFileField
from django.contrib.auth.models import User

<<<<<<< HEAD

class Tag(models.Model):
    """
    A Single Tag Entry
    Author: Rana El-Garem
    """
    tag = models.CharField(max_length=15, unique=True)

    def __unicode__(self):
        return unicode(self.tag)


=======
>>>>>>> master
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

