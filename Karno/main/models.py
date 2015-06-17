from django.db import models


class File(models.Model):
    file_uploaded = models.FileField(upload_to='%Y/%m/%d')
