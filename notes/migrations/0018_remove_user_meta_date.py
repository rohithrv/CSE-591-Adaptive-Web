# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-29 17:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0017_auto_20171129_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_meta',
            name='date',
        ),
    ]
