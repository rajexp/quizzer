# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-28 20:32
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0008_contribution_modified_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime(2017, 10, 28, 20, 32, 28, 615250, tzinfo=utc))),
                ('published', models.BooleanField(default=False)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('BIRTHDAY', 'BIRTHDAY'), ('CONTEST', 'CONTEST'), ('TRENDING', 'TRENDING'), ('QUIZ', 'QUIZ'), ('CHALLENGE', 'CHALLENGE'), ('POINTS', 'POINTS'), ('FOLLOW', 'FOLLOW'), ('NEW_CONTENT', 'NEW_CONTENT'), ('UNLOCK', 'UNLOCK')], max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('id_first', models.CharField(max_length=100)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('score', models.CharField(max_length=10)),
                ('name_second', models.CharField(max_length=50)),
                ('id_second', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(editable=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
