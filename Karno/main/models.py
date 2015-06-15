from django.db import models


class File(models.Model):
    file = models.FileField()
    file_type = models.CharField(max_length=50)

