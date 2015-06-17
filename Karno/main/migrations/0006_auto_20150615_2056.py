# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150615_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_uploaded',
            field=models.FileField(upload_to=b'%Y/%m/%d'),
        ),
    ]
