# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.RestrictedFileField


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150615_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_uploaded',
            field=main.RestrictedFileField.RestrictedFileField(upload_to=b'%Y/%m/%d'),
        ),
    ]
