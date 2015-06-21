# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.RestrictedFileField
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            ],
        ),
        migrations.CreateModel(
            name='GroupPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_uploaded', models.ForeignKey(to='main.File')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(unique=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=128)),
                ('video_id', models.CharField(max_length=128)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='tags',
            field=models.ManyToManyField(to='main.Tag'),
        ),
        migrations.AddField(
            model_name='file',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
