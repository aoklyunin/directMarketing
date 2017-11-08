import datetime

import django
from django.contrib.auth.models import User
from django.db import models


# класс исполнителя
from customer.models import MarketCamp
from mainApp.models import Comment


class Consumer(models.Model):
    # пользователь
    user = models.OneToOneField(User)
    # ссылка на VK
    vk_token = models.TextField(max_length=10000, default="")
    # id
    vk_id = models.IntegerField(default=0)
    # ссылка на инсту
    insta_link = models.TextField(max_length=10000, default="")
    # ссылка на инсту
    fb_link = models.TextField(max_length=10000, default="")
    # Баланс
    balance = models.FloatField(default=0)
    # Киви-кошелёк
    qiwi = models.TextField(max_length=100, default="")
    # автоматический вывод
    autoWithDraw = models.BooleanField(default=True)
    # автоматическое участие во всех кампаниях
    autoParticipate = models.BooleanField(default=False)
    # аудитория вк(кол-во друзей и подписчиков)
    vkCnt = models.IntegerField(default=0)
    # обработка аудитории
    vkProcessState = models.IntegerField(default=0)
    VK_PROCESS_STATES = ["Не обработан", "Запустилась обработка", "Обработка закончена"]
    VK_STATE_NOT_PROCESSED = 0
    VK_STATE_PROCESSED_NOW = 1
    VK_STATE_PROCESSED = 2


    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name


class WithdrawTransaction(models.Model):
    states = ['В обработке', 'Отклонена', 'Выполнена']
    list_states = ["Не обработанные заявки", "Отклонённые заявки", "Принятые заявки"]
    STATE_PROCESS = 0
    STATE_REJECTED = 1
    STATE_ACCEPTED = 2
    # комментарий транзакции
    tc = models.TextField(max_length=100, default="")
    comments = models.ManyToManyField(Comment)
    consumer = models.ForeignKey(Consumer)
    state = models.IntegerField(default=0)
    value = models.FloatField(default=0)
    dt = models.DateTimeField(default=django.utils.timezone.now())


class ConsumerMarketCamp(models.Model):
    # маркетинговая компания
    marketCamp = models.ForeignKey(MarketCamp)
    # просмотров от пользователя
    viewCnt = models.IntegerField(default=0)
    # id поста на странице пользователя
    postId = models.IntegerField(default=0)
    # сслыка на запись
    link = models.TextField(max_length=1000)
    # исполнитель
    consumer = models.ForeignKey(Consumer)
    # тип участи
    joinType = models.IntegerField(default=0)
    # типы участия
    joinTypes = ["Не участвую", "Участвую", "Участвовал"]
    # считерил
    stateCheated = models.IntegerField(default=0)

    TYPE_NOT_JOINED = 0
    TYPE_JOINED = 1
    TYPE_JOINED_NOW = 2

    STATE_NOT_CHEATED = 0
    STATE_PRETEND_CHEATED = 1
    STATE_CHEATED = 2

    def __str__(self):
        return str(self.marketCamp)+":"+str(self.viewCnt)+" "+str(self.postId)

    def __unicode__(self):
        return str(self.marketCamp) + ":" + str(self.viewCnt) + " " + str(self.postId)
