# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-30 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0019_cheatsheet_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheatsheet',
            name='cheatsheet_title',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='cheatsheet',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
