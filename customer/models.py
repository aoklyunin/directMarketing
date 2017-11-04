import datetime

import django
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

from mainApp.models import Comment
from mysite.settings import MEDIA_URL


class Customer(models.Model):
    companyName = models.TextField(max_length=1000, default="")
    user = models.OneToOneField(User)
    # Киви-кошелёк
    qiwi = models.TextField(max_length=100, default="")
    # Баланс
    balance = models.FloatField(default=0)


class ReplenishTransaction(models.Model):
    # делаем массив с заголовками для каждого из состояний
    list_states = ["Ожидающие оплаты заяки", "Не обработанные заявки", "Отклонённые заявки", "Принятые заявки"]
    states = ['Ожидает оплаты', 'В обработке', 'Отклонена', 'Выполнена']
    STATE_WAIT_FOR_PAY = 0
    STATE_PROCESS = 1
    STATE_REJECTED = 2
    STATE_ACCEPTED = 3
    # комментарий транзакции
    tc = models.TextField(max_length=100, default="")
    comments = models.ManyToManyField(Comment)
    customer = models.ForeignKey(Customer)
    state = models.IntegerField(default=0)
    value = models.FloatField(default=0)
    dt = models.DateTimeField(default=django.utils.timezone.now())


class MarketCamp(models.Model):
    # id группы ВК
    group_id = -155745173
    # platforms = ["-", "ВК", "Инстаграм", "FB"]
    platforms = ["-", "ВК"]
    # картинка для кампании
    image = models.ImageField(upload_to='', default="template.jpg")
    # желаемое описание
    description = models.TextField(max_length=100000)
    # цена просмотра
    viewPrice = models.FloatField(default=1)
    # бюджет
    budget = models.FloatField(default=0)
    # набор фраз, мб потом вообще регулярка
    phrases = models.TextField(max_length=100000, blank=True)
    # кол-во просмотров, сколько хотят
    targetViewCnt = models.IntegerField(default=0)
    # кол-во просмотров, сколько сейчас
    curViewCnt = models.IntegerField(default=0)
    # площадка
    platform = models.IntegerField(default=0)
    # возростной таргетинг: первый байт нижняя граница, второй - верхняя
    ageTarget = models.IntegerField(default=0)
    # таргетинг по городу или региону
    placeTarget = models.TextField(max_length=1000, blank=True)
    # заказчик
    customer = models.ForeignKey(Customer)
    # цена клика
    clickPrice = models.FloatField(default=0)
    # работает ли
    isActive = models.BooleanField(default=False)
    # старт
    startTime = models.DateTimeField(default=django.utils.timezone.now())
    # конец
    endTime = models.DateTimeField(default=django.utils.timezone.now())
    # админ одобрил
    adminApproved = models.IntegerField(default=0)
    # комментарии
    comments = models.ManyToManyField(Comment, blank=True, null=True)
    # id записи VK
    vkPostID = models.IntegerField(default=0)

    APPROVE_STATES = ["Обрабатывается", "Принята", "Отклонена"]

    STATE_PROCESS = 0
    STATE_APPROVED = 1
    STATE_NOT_APPROVED = 2

    PLATFORM_CHOICES = []
    for i in range(len(platforms)):
        PLATFORM_CHOICES.append((str(i), platforms[i]))

    def __str__(self):
        return str(self.vkPostID) + ":" + str(self.viewPrice) + " " + str(self.curViewCnt) + "/" + str(
            self.targetViewCnt)

    def __unicode__(self):
        return str(self.vkPostID) + ":" + str(self.viewPrice) + " " + str(self.curViewCnt) + "/" + str(
            self.targetViewCnt)
