import requests


def postVK(u):
    r = requests.get('https://api.vk.com/method/wall.post?owner_id='+str(u.vk_id)+"&message=test&access_token="+u.vk_token).json()
    return r
    #uid = r['response']['uid']


