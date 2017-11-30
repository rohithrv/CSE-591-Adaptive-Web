# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
import uuid

from django.utils.datetime_safe import datetime
from django.utils.timezone import now

from django.db import models

# Create your models here.
from django.db import models


class userLogin(models.Model):
    authorid = models.CharField(max_length=20)
    logdate = models.DateTimeField()


class userRating(models.Model):
    username = models.CharField(max_length=20)
    userrating = models.PositiveIntegerField()


class CheatSheet(models.Model):
    cheatsheet_title = models.CharField(max_length=100, default=" ")
    user_id = models.CharField(max_length=100)
    note_id = models.PositiveIntegerField(primary_key=True)
    position = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=100, default=" ")
    content = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now)


class user_meta(models.Model):
    user_id = models.CharField(primary_key=True,max_length=100)
    tags = models.CharField(max_length=5000, default=" ")
    titles = models.CharField(max_length=1000, default=" ")


class note_meta(models.Model):
    note_id = models.PositiveIntegerField(primary_key=True)
    tags = models.CharField(max_length=5000, default=" ")
    title = models.CharField(max_length=1000, default=" ")


class TagNotes(models.Model):
    noteid = models.PositiveIntegerField(primary_key=True)
    username = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now)


class Likes(models.Model):
    voted_user = models.CharField(max_length=20)
    noteid = models.PositiveIntegerField()


# add note datetime
class notes(models.Model):
    noteid = models.AutoField(primary_key=True)
    authorid = models.PositiveIntegerField()
    type = models.PositiveIntegerField()
    points = models.IntegerField(default=0, blank=True)
    upvote = models.IntegerField(default=0, blank=True)
    downvote = models.IntegerField(default=0, blank=True)
    tagged = models.PositiveIntegerField(default=0)
    username = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.noteid + ' - ' + self.title
