# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from notes.models import *
from django.contrib import admin

# Register your models here.
admin.site.register(userLogin)
admin.site.register(userRating)
admin.site.register(notes)
admin.site.register(TagNotes)
admin.site.register(user_meta)
admin.site.register(note_meta)
admin.site.register(CheatSheet)
admin.site.register(CheatSheets)