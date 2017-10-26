import requests
import time


def postVK(u):
    r = requests.get('https://api.vk.com/method/wall.post?owner_id=' + str(
        u.vk_id) + "&message=test&access_token=" + u.vk_token + "&count=10").json()
    return r
    # uid = r['response']['uid']


def getReposts(u, token):
    arr = []
    r = requests.get('https://api.vk.com/method/wall.get?owner_id=' + str(u) + "&access_token=" + token).json()
    for c in r['response'][1:]:
        print(c)
        try:
            arr.append({"cpid": c['copy_post_id'], "copy_owner_id": c['copy_owner_id'],
                       "id": c['id']})
        except:
            pass
    return arr



def leaveCampany(mc):
    mc.joinType = 2
    mc.worker.balance += mc.viewCnt*mc.marketCamp.viewPrice
    mc.worker.save()
    mc.save()
