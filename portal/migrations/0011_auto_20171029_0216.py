# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-28 20:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0010_auto_20171029_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
