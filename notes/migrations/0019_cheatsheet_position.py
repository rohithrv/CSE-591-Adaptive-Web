# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-30 03:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0018_remove_user_meta_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cheatsheet',
            name='position',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
