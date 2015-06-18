from django.db import models


class File(models.Model):
    file_uploaded = models.FileField(upload_to='%Y/%m/%d')


class AudioFile(models.Model):
    title = models.CharField(max_length=32)
    artist = models.CharField(max_length=12)
    genre = models.CharField(max_length=12)
    source_file = models.ForeignKey(File)
