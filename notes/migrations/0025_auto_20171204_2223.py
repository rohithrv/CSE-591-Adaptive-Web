# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-04 22:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0024_auto_20171130_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='authorid',
            field=models.CharField(max_length=20),
        ),
    ]
