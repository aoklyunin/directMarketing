import requests
from django.shortcuts import render

from consumer.views import consumerError
from mysite import settings
from django.http import HttpResponseRedirect

from consumer.localCode import postVK
from consumer.models import Consumer

href = 'http://directpr.herokuapp.com'


def getCode(request):
    return HttpResponseRedirect(
        'http://oauth.vk.com/authorize?client_id=' + settings.VK_APP_ID +
        '&redirect_uri=' + href +
        '/consumer/vk/processCode/&response_type=code&scope=wall,offline,friends,photos,audio,')


def processCode(request):
    try:
        us = Consumer.objects.get(user=request.user)
    except:
        return consumerError(request)

    try:
        code = request.GET["code"]
        r = requests.get('https://oauth.vk.com/access_token?client_id=' + settings.VK_APP_ID +
                         '&client_secret=' + settings.VK_API_SECRET + '&redirect_uri=' + href +
                         '/consumer/vk/processCode/&code=' + code).json()
        us.vk_token = r["access_token"]
        us.vk_id = int(r["user_id"])
        us.save()

        return HttpResponseRedirect('/consumer/')
    except:
        return HttpResponseRedirect('/consumer/')


def postVKview(request):
    try:
        u = Consumer.objects.get(user=request.user)
    except:
        return consumerError(request)

    r = postVK(u)

    template = 'mainApp/result_page.html'
    context = {
        "text": r,
    }
    return render(request, template, context)
