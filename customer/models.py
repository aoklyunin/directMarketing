import datetime

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
    states = ['Ожидает оплаты', 'В обработке', 'Отклонена', 'Выполнена']
    # комментарий транзакции
    tc = models.TextField(max_length=100, default="")
    comments = models.ManyToManyField(Comment)
    customer = models.ForeignKey(Customer)
    state = models.IntegerField(default=0)
    value = models.FloatField(default=0)
    dt = models.DateTimeField(default=datetime.datetime.now())


class MarketCamp(models.Model):
    platforms = ["-", "ВК", "Инстаграм", "FB"]
    # картинка для кампании
    image = models.ImageField(upload_to='', default="template.jpg")
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
    # цена клика
    clickPrice = models.FloatField(default=0)
    # работает ли
    isActive = models.BooleanField(default=False)
    # старт
    startTime = models.DateTimeField(default=datetime.datetime.now())
    # конец
    endTime = models.DateTimeField(default=datetime.datetime.now())
    # админ одобрил
    adminApproved = models.BooleanField(default=False)

    PLATFORM_CHOICES = []
    for i in range(len(platforms)):
        PLATFORM_CHOICES.append((str(i), platforms[i]))