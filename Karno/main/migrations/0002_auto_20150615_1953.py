# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='file_type',
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=b'documents/%Y/%m/%d'),
        ),
    ]
