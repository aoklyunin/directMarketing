# -*- coding: utf-8 -*-
import csv
import random
import string
from datetime import datetime

import six
from dateutil.parser import parse

import re
import requests
import time
import numpy as np
import scipy.stats as st
from urllib.request import urlopen

from dateutil.relativedelta import relativedelta
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from adminPanel.models import AdminUser
from consumer.models import Consumer, ConsumerMarketCamp
from customer.models import Customer, MarketCamp
from django.core.mail import send_mail


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


def checkToken(vk_token):
    print(vkRequest('secure.checkToken',{'token':vk_token}))
    return  False


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
    if len(dates) == 0:
        return -1000
    dates.sort()
    dd = [j - i for i, j in zip(dates[:-1], dates[1:])]
    return round(st.kurtosis(dd), 2)


def getFriendsUsers(id, token, lst):
    res = vkRequest("friends.get", {"count": "1", "user_id": str(id), "access_token": token})

    cnt = 0

    for i in range(int(res['response']['count'] / 1000) + 1):
        #   print(i)
        res = vkRequest("friends.get",
                        {"count": "1000", "offset": str(i * 1000), "user_id": str(id), "access_token": token})
        try:
            for r in res['response']['items']:
                try:
                    if r not in lst:
                        ucd = getUserCreatedDate(r)
                        if ucd > 100:
                            k = checkBotUser(r, token)
                            if k < -0.1:
                                print("https://vk.com/id" + str(r) + " " + str(k))
                            else:
                                cnt += 1
                        else:
                            print("https://vk.com/id" + str(r) + " " + str(k))
                except:
                    pass
        except:
            pass
    return cnt


def getFollowersUsers(id, token, lst):
    res = vkRequest("users.getFollowers", {"count": "1", "user_id": str(id), "access_token": token})

    cnt = 0

    for i in range(int(res['response']['count'] / 1000) + 1):
        #   print(i)
        res = vkRequest("users.getFollowers",
                        {"count": "1000", "offset": str(i * 1000), "user_id": str(id), "access_token": token})
        try:
            for r in res['response']['items']:
                try:
                    if r not in lst:
                        ucd = getUserCreatedDate(r)
                        # print(ucd)
                        if ucd > 100:
                            k = checkBotUser(r, token)
                            if k < -0.1:
                                print("https://vk.com/id" + str(r) + " " + str(k))
                            else:
                                cnt += 1
                        else:
                            print("https://vk.com/id" + str(r) + " " + str(k))
                except:
                    pass
        except:
            pass
    return cnt


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


def getUserCreatedDate(id):
    req = 'http://vk.com/foaf.php?id=' + str(id)
    # print(req)
    content = urlopen(req).read()

    result = re.findall(r'ya:created dc:date="[0-9]+-[0-9]+-[0-9]+T[0-9]+:[0-9]+:[0-9]+\+[0-9]+:[0-9]+"', str(content))
    # print(result[0][20:45])
    dt = parse(result[0][20:45])

    return (datetime.now() - dt.replace(tzinfo=None)).days


def closeMarketCamp(mc):
    delta = mc.targetViewCnt - mc.curViewCnt
    if delta < 0:
        cmCnt = ConsumerMarketCamp.objects.filter(marketCamp=mc).count()
        minusCnt = cmCnt / abs(delta)
    else:
        minusCnt = 0

    for cm in ConsumerMarketCamp.objects.filter(marketCamp=mc):
        leaveCampany(cm.consumer, minusCnt)

    mc.isActive = False
    mc.save()


def test():
    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['aoklyunin@gmail.com'],
        fail_silently=False,
    )


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) + six.text_type(user.is_active)


account_activation_token = AccountActivationTokenGenerator()

def genRandomString(n):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


def postVK(u):
    r = requests.get('https://api.vk.com/method/wall.post?owner_id=' + str(
        u.vk_id) + "&message=test&access_token=" + u.vk_token + "&count=10").json()
    time.sleep(0.3)
    return r
    # uid = r['response']['uid']


def getReposts(u, token):
    arr = []
    r = requests.get('https://api.vk.com/method/wall.get?owner_id=' + str(u) + "&access_token=" + token).json()
    time.sleep(0.3)
    for c in r['response'][1:]:
        # print(c)
        try:
            arr.append({"cpid": c['copy_post_id'], "copy_owner_id": c['copy_owner_id'],
                        "id": c['id']})
        except:
            pass
    return arr


def getRepostedCompanies(u, token):
    reposts = getReposts(u, token)
    lstM = []
    lstID = []
    for m in MarketCamp.objects.filter(isActive=True):
        for r in reposts:
            if (m.vkPostID == r["cpid"]) and (r["copy_owner_id"] == MarketCamp.group_id):
                lstM.append(m)
                lstID.append(r["id"])
    return [lstM, lstID]


def getNotRepostedCompanies(lstRM):
    lst = []
    lstM = []
    for r in lstRM:
        lst.append(r.pk)
    for m in MarketCamp.objects.filer(isActive=True).exclude(pk__in=lst):
        lstM.append(m)
    return [lstM]


def leaveCampany(mc,minusCnt=0):
    print("Leave company called")
    mc.joinType = 2
    if mc.cheated == ConsumerMarketCamp.STATE_NOT_CHEATED:
        mc.consumer.balance += (mc.viewCnt-minusCnt) * mc.marketCamp.viewPrice
    mc.consumer.save()
    mc.save()
    print("saved")


def getViewCnt(id, post_id, token):
    r = requests.get('https://api.vk.com/method/wall.getById?posts=' + str(id) + '_' + str(
        post_id) + "&access_token=" + token + "&v=5.69").json()
    time.sleep(0.3)
    return int(r['response'][0]['views']['count'])



