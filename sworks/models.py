# -*- coding: utf-8 -*-
# модели Django
from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# класс студента
class Student(models.Model):
    # пользователь
    user = models.OneToOneField(User)
    # класс
    github_rep = models.CharField(max_length=200)
    # группа
    st_group = models.CharField(max_length=200)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + '(' + str(
            self.st_group) + ')'

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name


# комментарий к попытке
class AttemptComment(models.Model):
    class Meta:
        ordering = ['-datetime']

    # прочитан или нет
    isReaded = models.BooleanField(default=False)
    # текст комментария
    text = models.TextField(max_length=100000)
    # автор комментария
    author = models.ForeignKey(Student)
    # дата написания
    datetime = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.text

    def __unicode__(self):
        return self.text


# задание
class Task(models.Model):
    # имя задания
    task_name = models.CharField(max_length=200)
    # кода выложено
    pub_date = models.DateField('date published')

    def __str__(self):
        return self.task_name + '(' + str(self.pub_date) + ')'

    def __unicode__(self):
        return self.task_name


# попытка
class Mark(models.Model):
    # задание
    task = models.ForeignKey(Task)
    # оценка
    m_value = models.IntegerField(default=0)
    # дата добавления
    add_date = models.DateTimeField(default=datetime.datetime.now())
    # проверена ли оценка
    state = models.IntegerField(default=0)
    # комментарии к попытке
    comment = models.ManyToManyField(AttemptComment)
    # кто оставил
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.task.task_name + '(' + str(self.add_date) + ') ' + str(self.m_value)

    def __unicode__(self):
        return self.task.task_name + '(' + str(self.add_date) + ' ' + str(self.m_value)


class InfoText(models.Model):
    text = models.TextField(max_length=100000, null=True, blank=True)
    subText = models.TextField(max_length=100000, null=True, blank=True)
    appendText = models.TextField(max_length=100000, null=True, blank=True)
    caption = models.TextField(max_length=100000, null=True, blank=True)
    pageName = models.TextField(max_length=100000, null=True, blank=True)

    def __str__(self):
        return self.pageName
