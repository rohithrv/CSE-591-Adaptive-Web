# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-20 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_auto_20171120_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='type',
            field=models.PositiveIntegerField(),
        ),
    ]