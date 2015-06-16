# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_uploaded',
            field=models.ImageField(upload_to=b'%Y/%m/%d'),
        ),
    ]
