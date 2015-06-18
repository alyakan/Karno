from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    file = models.FileField()
    file_type = models.CharField(max_length=50)


class YoutubeUrl(models.Model):
    """
    Represents a single existing Youtube Url to be embeded

    Author: Aly Yakan

    """
    url = models.CharField(max_length=128, null=False)
    video_id = models.CharField(max_length=128)
    user = models.ForeignKey(User)
