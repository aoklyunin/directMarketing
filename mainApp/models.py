# -*- coding: utf-8 -*-
# модели Django
from __future__ import unicode_literals

import datetime

import django
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Comment(models.Model):
    author = models.ForeignKey(User, related_name="author", default=None, blank=True, null=True)
    text = models.TextField(max_length=10000, default="")
    image = models.ImageField()
    dt = models.DateTimeField(default=django.utils.timezone.now())
    target = models.ForeignKey(User, related_name="target", default=None, blank=True, null=True)
    theme = models.CharField(default="", max_length=200)
    readed = models.BooleanField(default=False)


class InfoText(models.Model):
    text = models.TextField(max_length=100000, null=True, blank=True)
    subText = models.TextField(max_length=100000, null=True, blank=True)
    appendText = models.TextField(max_length=100000, null=True, blank=True)
    caption = models.TextField(max_length=100000, null=True, blank=True)
    pageName = models.TextField(max_length=100000, null=True, blank=True)

    def __str__(self):
        return self.pageName


# заявка в тех. поддержку
class TehSupport(models.Model):
    STATE_OPENED = 0
    STATE_CLOSED = 1
    states = ["Открытые", "Закрытые"]
    author = models.ForeignKey(User)
    comments = models.ManyToManyField(Comment)
    state = models.IntegerField(default=0)
    dt = models.DateTimeField(default=django.utils.timezone.now())
