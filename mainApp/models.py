# -*- coding: utf-8 -*-
# модели Django
from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# класс исполнителя
class Consumer(models.Model):
    # пользователь
    user = models.OneToOneField(User)
    # ссылка на VK
    vk_link = models.TextField(max_length=10000,default="")
    # ссылка на инсту
    insta_link = models.TextField(max_length=10000, default="")
    # ссылка на инсту
    fb_link = models.TextField(max_length=10000,default="")
    # Баланс
    balance = models.IntegerField(default=0)
    # Киви-кошелёк
    qiwi = models.TextField(max_length=100,default="")

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + '(' + str(
            self.st_group) + ')'

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Customer(models.Model):
    companyName = models.TextField(max_length=1000, default="")
    user = models.OneToOneField(User)
    # Киви-кошелёк
    qiwi = models.TextField(max_length=100, default="")
    # Баланс
    balance = models.IntegerField(default=0)


class MarketCamp(models.Model):
    platforms = ["ВК", "Инстаграм", "FB"]

    # картинка для кампании
    image = models.ImageField()
    # желаемое описание
    description = models.TextField(max_length=100000)
    # цена просмотра
    viewPrice = models.FloatField(default=1)
    # бюджет
    budget = models.FloatField(default=0)
    # набор фраз, мб потом вообще регулярка
    phrases = models.TextField(max_length=100000)
    # кол-во просмотров, сколько хотят
    targetViewCnt = models.IntegerField(default=0)
    # кол-во просмотров, сколько сейчас
    curViewCnt = models.IntegerField(default=0)
    # площадка
    platform = models.IntegerField(default=0)
    # возростной таргетинг: первый байт нижняя граница, второй - верхняя
    ageTarget = models.IntegerField(default=0)
    # таргетинг по городу или региону
    placeTarget = models.TextField(max_length=1000)
    # заказчик
    customer = models.ForeignKey(Customer)


class WorkerMarketCamp(models.Model):
    # маркетинговая компания
    marketCamp = models.ForeignKey(MarketCamp)
    # просмотров от пользователя
    viewCnt = models.IntegerField(default=0)
    # сслыка на запись
    link = models.TextField(max_length=1000)
    # исполнитель
    worker = models.ForeignKey(Consumer)


class Admin(models.Model):
    # пользователь
    user = models.OneToOneField(User)


class InfoText(models.Model):
    text = models.TextField(max_length=100000, null=True, blank=True)
    subText = models.TextField(max_length=100000, null=True, blank=True)
    appendText = models.TextField(max_length=100000, null=True, blank=True)
    caption = models.TextField(max_length=100000, null=True, blank=True)
    pageName = models.TextField(max_length=100000, null=True, blank=True)

    def __str__(self):
        return self.pageName
