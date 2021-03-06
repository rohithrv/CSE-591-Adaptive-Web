# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-29 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0016_auto_20171129_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheatSheet',
            fields=[
                ('user_id', models.CharField(max_length=100)),
                ('note_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('cheatsheet_title', models.CharField(default=' ', max_length=100)),
                ('title', models.CharField(default=' ', max_length=100)),
                ('content', models.CharField(max_length=10000)),
                ('date', models.DateTimeField(default=django.utils.datetime_safe.datetime.now)),
            ],
        ),
        migrations.AddField(
            model_name='user_meta',
            name='date',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now),
        ),
        migrations.AlterField(
            model_name='user_meta',
            name='user_id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
