import datetime

from django.contrib.auth.models import User
from django.db import models


# класс исполнителя
from customer.models import MarketCamp
from mainApp.models import Comment


class Consumer(models.Model):
    # пользователь
    user = models.OneToOneField(User)
    # ссылка на VK
    vk_link = models.TextField(max_length=10000, default="")
    # ссылка на инсту
    insta_link = models.TextField(max_length=10000, default="")
    # ссылка на инсту
    fb_link = models.TextField(max_length=10000, default="")
    # Баланс
    balance = models.FloatField(default=0)
    # Киви-кошелёк
    qiwi = models.TextField(max_length=100, default="")

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name


class WithdrawTransaction(models.Model):
    states = ['В обработке', 'Отклонена', 'Выполнена']
    # комментарий транзакции
    tc = models.TextField(max_length=100, default="")
    comments = models.ManyToManyField(Comment)
    consumer = models.ForeignKey(Consumer)
    state = models.IntegerField(default=0)
    value = models.FloatField(default=0)
    dt = models.DateTimeField(default=datetime.datetime.now())


class ConsumerMarketCamp(models.Model):
    # маркетинговая компания
    marketCamp = models.ForeignKey(MarketCamp)
    # просмотров от пользователя
    viewCnt = models.IntegerField(default=0)
    # сслыка на запись
    link = models.TextField(max_length=1000)
    # исполнитель
    worker = models.ForeignKey(Consumer)
    # тип участи
    joinType = models.IntegerField(default=0)
    # типы участия
    joinTypes = ["Не участвую", "Участвую", "Участвовал"]
