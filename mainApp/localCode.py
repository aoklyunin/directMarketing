# -*- coding: utf-8 -*-
import csv
from datetime import datetime
import requests
import time
import numpy as np
import scipy.stats as st

from adminPanel.models import AdminUser
from consumer.models import Consumer
from customer.models import Customer


# бот вк 79854490925:ZsePLV1nXg
# id 453386628

# Распределение оценивается как предположительно близкое к нормальному,
# если установлено, что от 50 до 80 % всех значений располагаются в пределах
# одного стандартного отклонения от среднего арифметического,
# и коэффициент эксцесса по абсолютной величине не превышает значения равного двум.

def vkRequest(method, params):
    req = 'https://api.vk.com/method/' + method + "?"
    for k in params.keys():
        req += k + "=" + params[k] + "&"
    res = requests.get(req + "v=5.69").json()
    time.sleep(0.34)
    return res


def getImages(id, token):
    res = vkRequest("photos.getAlbums", {"need_system": "1", "owner_id": str(id), "access_token": token})
    a_ids = []
    for a in res['response']['items']:
        a_ids.append(a['id'])

    dates = []

    for aid in a_ids:
        res = vkRequest('photos.get',
                        {"extended": "1", "album_id": str(aid), "owner_id": str(id), "access_token": token})
        for r in res['response']['items']:
            dates.append(r['date'])
    dates.sort()

    dd = [j - i for i, j in zip(dates[:-1], dates[1:])]
    return round(st.kurtosis(dd), 2)


def getFriendsUsers(id, token):
    res = vkRequest("friends.get", {"count": "1", "user_id": str(id), "access_token": token})

    cnt = 0

    for i in range(int(res['response']['count'] / 1000) + 1):
        #   print(i)
        res = vkRequest("friends.get",
                        {"count": "1000", "offset": str(i * 1000), "user_id": str(id), "access_token": token})
        try:
            for r in res['response']['items']:
                try:
                    k = checkBotUser(r, token)
                    if k < 0:
                        print("https://vk.com/id" + str(r) + " " + str(k))
                    else:
                        cnt += 1
                except:
                    pass
        except:
            pass
    return cnt


def getSubscribersUsers(id, token):
    lst = []
    res = vkRequest("friends.get", {"count": "1", "user_id": str(id), "access_token": token})
    # print(res['response']['count'])

    for i in range(int(res['response']['count'] / 1000) + 1):
        #   print(i)
        res = vkRequest("friends.get",
                        {"count": "1000", "offset": str(i * 1000), "user_id": str(id), "access_token": token})
        try:
            for r in res['response']['items']:
                try:
                    k = checkBotUser(r, token)
                    if k < 0:
                        print("https://vk.com/id" + str(r) + " " + str(k))
                except:
                    pass
        except:
            pass
    return lst


def checkBotUser(id, token):
    return getImages(id, token)


def getUsType(user):
    try:
        Customer.objects.get(user=user)
        return 1
    except:
        try:
            Consumer.objects.get(user=user)
            return 2
        except:
            try:
                AdminUser.objects.get(user=user)
                return 3
            except:
                return 0
