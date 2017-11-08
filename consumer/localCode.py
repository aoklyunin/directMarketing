import requests
import time

from consumer.models import ConsumerMarketCamp
from customer.models import MarketCamp


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
    for m in MarketCamp.objects.all():
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
    for m in MarketCamp.objects.exclude(pk__in=lst):
        lstM.append(m)
    return [lstM]


def leaveCampany(mc):
    print("Leave company called")
    mc.joinType = 2
    mc.consumer.balance += mc.viewCnt * mc.marketCamp.viewPrice
    mc.consumer.save()
    mc.save()
    print("saved")


def getViewCnt(id, post_id, token):
    r = requests.get('https://api.vk.com/method/wall.getById?posts=' + str(id) + '_' + str(
        post_id) + "&access_token=" + token + "&v=5.69").json()
    time.sleep(0.3)
    return int(r['response'][0]['views']['count'])


