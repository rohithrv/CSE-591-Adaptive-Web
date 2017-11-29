# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-28 00:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0009_auto_20171121_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='points',
        ),
        migrations.AlterField(
            model_name='notes',
            name='date',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now),
        ),
    ]