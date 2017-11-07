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


def analyse(data):
    res = {}
    res["max"] = np.max(data)  # минимальное
    res["min"] = np.min(data)  # максимальное
    res["mean"] = round(np.mean(data), 2)  # среднее
    res["std"] = round(np.std(data), 2)  # CТО
    res["skew"] = round(st.skew(data), 2)  # ассиметрия
    res["kurtosis"] = round(st.kurtosis(data), 2)  # эксцесс
    res["variation"] = round(st.variation(data), 2)  # вариация
    return res


def getImages(id, token):
    res = vkRequest("photos.getAlbums", {"need_system": "1", "owner_id": str(id), "access_token": token})
    a_ids = []
    for a in res['response']['items']:
        a_ids.append(a['id'])

    dates = []
    # comments = []
    # likes = []

    for aid in a_ids:
        res = vkRequest('photos.get',
                        {"extended": "1", "album_id": str(aid), "owner_id": str(id), "access_token": token})
        for r in res['response']['items']:
            dates.append(r['date'])
            #    comments.append(r['comments']['count'])
            #     likes.append(r['likes']['count'])

    # dates.append(time.mktime(datetime.now().timetuple()))
    dmax = np.max(dates)
    dmin = np.min(dates)
    res = {}
    dates.sort()

    dd = [j - i for i, j in zip(dates[:-1], dates[1:])]
    # print(dd)
    res["dates"] = analyse(dd)
    res["dates"]["max"] = dmax
    res["dates"]["min"] = dmin
    # res["comments"] = analyse(comments)
    # res["likes"] = analyse(likes)
    res["len"] = len(dates)
    return res


def getPosts(id, token):
    res = vkRequest("wall.get", {"owner_id": str(id), "access_token": token})

    dates = []
    #  comments = []
    # # likes = []
    # views = []
    # from_ids = []
    # textes = 0

    cnt = len(res['response']['items'])
    for a in res['response']['items']:
        dates.append(a['date'])
        #   comments.append(a['comments']['count'])
        #   likes.append(a['likes']['count'])
        #   try:
        #       views.append(a['views']['count'])
        #  except:
        #       pass
        #   f = a["from_id"]
        #   if not f in from_ids:
        #       from_ids.append(f)
        #   if not a['text'] == "":
        #      textes += 1

    dmax = np.max(dates)
    dmin = np.min(dates)
    res = {}
    dates.sort()
    dd = [j - i for i, j in zip(dates[:-1], dates[1:])]
    res["dates"] = analyse(dd)
    res["dates"]["max"] = dmax
    res["dates"]["min"] = dmin
    #  res["comments"] = analyse(comments)
    #    res["likes"] = analyse(likes)
    #   res["views"] = analyse(views)
    res["len"] = cnt
    #  res["from_ids"] = len(from_ids)
    #  res["textCnt"] = cnt
    return res


def getGroupUsers(gid, token):
    with open("stats", "w", newline="\n") as file:
        writer = csv.writer(file)
        writer.writerow(["img_date_skew", "img_date_variation", "img_date_kutrosis",
                         "post_date_skew", "post_date_variation", "post_date_kutrosis"])

        res = vkRequest("groups.getMembers", {"count": "1", "group_id": str(gid), "access_token": token})
        lst = []
        print(res['response']['count'])
        for i in range(int(res['response']['count'] / 1000) + 1):
            print(i)
            res = vkRequest("groups.getMembers",
                            {"count": "1000", "offset": str(i * 1000), "group_id": str(gid), "access_token": token})
            try:
                for r in res['response']['items']:
                    try:
                        print(r)
                        writer.writerow(checkBotUser(int(r), token))
                    except:
                        pass
            except:
                print("error")
                print(res)


def getFriendsUsers(id, token):
    lst = []
    res = vkRequest("friends.get", {"count": "1", "user_id": str(id), "access_token": token})
    print(res['response']['count'])

    for i in range(int(res['response']['count'] / 1000) + 1):
        print(i)
        res = vkRequest("friends.get",
                        {"count": "1000", "offset": str(i * 1000), "user_id": str(id), "access_token": token})
        try:
            for r in res['response']['items']:
                print(r)
                try:
                    lst.append(checkBotUser(r, token))
                except:
                    pass
        except:
            print("error")
            print(res)


    with open("stats", "w", newline="\n") as file:
        writer = csv.writer(file)
        writer.writerow(["img_date_skew", "img_date_variation", "img_date_kutrosis",
                     "post_date_skew", "post_date_variation", "post_date_kutrosis"])
        writer.writerows(lst)


def checkBotUser(id, token):
    images = getImages(id, token)
    posts = getPosts(id, token)

    return [images["dates"]["skew"], images["dates"]["variation"], images["dates"]["kurtosis"],
            posts["dates"]["skew"], posts["dates"]["variation"], posts["dates"]["kurtosis"],
            " https://vk.com/id" + str(id)]


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
