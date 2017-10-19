# -*- coding: utf-8 -*-
# модели Django
from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



class Comment(models.Model):
    author = models.ForeignKey(User)
    text = models.TextField(max_length=10000, default="")
    image = models.ImageField()
    dt = models.DateTimeField(default=datetime.datetime.now())




class InfoText(models.Model):
    text = models.TextField(max_length=100000, null=True, blank=True)
    subText = models.TextField(max_length=100000, null=True, blank=True)
    appendText = models.TextField(max_length=100000, null=True, blank=True)
    caption = models.TextField(max_length=100000, null=True, blank=True)
    pageName = models.TextField(max_length=100000, null=True, blank=True)

    def __str__(self):
        return self.pageName
