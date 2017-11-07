# -*- coding: utf-8 -*-
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
    time.sleep(0.3)
    return res


def analyse(data):
    res = {}
    res["max"] = np.max(data)  # минимальное
    res["min"] = np.min(data)  # максимальное
    res["mean"] = np.mean(data)  # среднее
    res["std"] = np.std(data)  # CТО
    res["skew"] = st.skew(data)  # ассиметрия
    res["kurtosis"] = st.kurtosis(data)  # эксцесс
    res["variation"] = st.variation(data)  # вариация
    return res


def getImages(id, token):
    res = vkRequest("photos.getAlbums", {"need_system": "1", "owner_id": str(id), "access_token": token})
    a_ids = []
    for a in res['response']['items']:
        a_ids.append(a['id'])

    dates = []
    comments = []
    linkes = []

    for aid in a_ids:
        res = vkRequest('photos.get',
                        {"extended": "1", "album_id": str(aid), "owner_id": str(id), "access_token": token})
        for r in res['response']['items']:
            dates.append(r['date'])
            comments.append(r['comments']['count'])
            linkes.append(r['likes']['count'])

    #dates.append(time.mktime(datetime.now().timetuple()))
    max = np.max(dates)
    min = np.min(dates)
    res = {}
    dates.sort()

    dd = [j - i for i, j in zip(dates[:-1], dates[1:])]
    #print(dd)
    res["dates"] = analyse(dd)
    res["dates"]["max"] = max
    res["dates"]["min"] = min
    res["comments"] = analyse(comments)
    res["linkes"] = analyse(linkes)
    res["len"] = len(dates)
    return res


def getPosts(id, token):
    res = vkRequest("photos.getAlbums", {"need_system": "1", "owner_id": str(id), "access_token": token})
    a_ids = []
    for a in res['response']['items']:
        a_ids.append(a['id'])

    dates = []
    comments = []
    linkes = []

    for aid in a_ids:
        res = vkRequest('photos.get',
                        {"extended": "1", "album_id": str(aid), "owner_id": str(id), "access_token": token})
        for r in res['response']['items']:
            dates.append(r['date'])
            comments.append(r['comments']['count'])
            linkes.append(r['likes']['count'])

    dates.append(time.mktime(datetime.now().timetuple()))
    max = np.max(dates)
    min = np.min(dates)
    res = {}
    dates.sort()
    dd = [j - i for i, j in zip(dates[:-1], dates[1:])]
    print(dd)
    res["dates"] = analyse(dd)
    res["dates"]["max"] = max
    res["dates"]["min"] = min
    res["comments"] = analyse(comments)
    res["linkes"] = analyse(linkes)
    res["len"] = len(dates)
    return res


def checkBotUser(id,token):
    #print(getImages(id, token))
    print(getImages(id, token))



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
