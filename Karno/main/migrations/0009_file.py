# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.RestrictedFileField
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_delete_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_uploaded', main.RestrictedFileField.RestrictedFileField(upload_to=b'%Y/%m/%d')),
                ('public', models.BooleanField(default=False)),
                ('registered_users', models.BooleanField(default=False)),
                ('group', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
