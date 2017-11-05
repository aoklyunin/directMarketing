# -*- coding: utf-8 -*-
import requests
import time

from adminPanel.models import AdminUser
from consumer.models import Consumer
from customer.models import Customer

def getImages(id,token):
        arr = []
        r = requests.get('https://api.vk.com/method/photos.getAll?owner_id=' + str(id) + "&access_token=" + token).json()
        time.sleep(0.3)
        print(r)
        #for c in r['response'][1:]:
            # print(c)
         #   try:
          #      arr.append({"cpid": c['copy_post_id'], "copy_owner_id": c['copy_owner_id'],
           #                 "id": c['id']})
            #except:
        #        pass
       # return arr
        return []

def checkBotUser(u):
    return getImages(u.vk_id,u.vk_token)


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

