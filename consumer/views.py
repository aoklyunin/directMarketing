import json

import requests
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.

from consumer.form import ConsumerForm
from consumer.localCode import postVK, getReposts, leaveCampany, getRepostedCompanies, getViewCnt
from consumer.models import Consumer, WithdrawTransaction, ConsumerMarketCamp
from customer.forms import MarketCampForm
from customer.models import Customer, ReplenishTransaction, MarketCamp
from mainApp.code import is_member
from mainApp.forms import PaymentForm, TextForm
from mainApp.models import Comment
from mysite import settings

from django.shortcuts import redirect


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    try:
        us = Consumer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = ConsumerForm(request.POST)

        if form.is_valid():
            us.qiwi = form.cleaned_data['qiwi']
            us.user.first_name = form.cleaned_data['name']
            us.user.last_name = form.cleaned_data['second_name']
            us.user.save()
            us.autoParticipate = form.cleaned_data['autoParticipate']
            us.save()

    form = ConsumerForm(initial={'name': us.user.first_name, 'second_name': us.user.last_name,
                                 'qiwi': us.qiwi, 'autoParticipate': us.autoParticipate})
    template = 'consumer/index.html'

    try:
        r = requests.get('https://api.vk.com/method/users.get?user_ids=' + str(us.vk_id) + "&access_token=" + str(
            us.vk_token)).json()
        uid = r['response'][0]['uid']
    except:
        uid = 0

    context = {
        "u": us,
        "uid": uid,
        "form": form,
    }
    return render(request, template, context)


def balance(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    try:
        u = Consumer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    ts = WithdrawTransaction.objects.filter(consumer=u).order_by('dt')
    transactions = []
    for t in ts:
        transactions.append({"date": t.dt, "value": t.value, "state": WithdrawTransaction.states[t.state],
                             "tid": t.id})
    template = 'consumer/balance.html'
    context = {
        "u": u,
        "transactions": transactions,
    }
    return render(request, template, context)


def withdraw(request):
    try:
        u = Consumer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = PaymentForm(request.POST)
        if form.is_valid():
            t = WithdrawTransaction.objects.create(consumer=u, value=form.cleaned_data["value"])
            return HttpResponseRedirect('/consumer/balance/')

    template = 'consumer/withdraw.html'
    context = {
        "form": PaymentForm(),
    }
    return render(request, template, context)


def autoWithdraw(request, tp):
    try:
        u = Consumer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    u.autoWithDraw = tp == '1'
    u.save()

    return HttpResponseRedirect('/consumer/balance/')


def withdraw_detail(request, tid):
    ct = WithdrawTransaction.objects.get(id=tid)
    if not (is_member(request.user, "admins") or request.user == ct.consumer.user):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = TextForm(request.POST)
        if form.is_valid():
            c = Comment.objects.create(author=request.user, text=form.cleaned_data["value"])
            ct.comments.add(c)

    template = 'consumer/withdraw_detail.html'
    context = {
        "id": tid,
        "need_pay": ct.state == 0,
        "date": ct.dt.strftime("%d.%m.%y"),
        "state": WithdrawTransaction.states[ct.state],
        "comments": ct.comments.order_by('dt'),
        "form": TextForm(),
    }
    return render(request, template, context)


def terms(request):
    template = 'consumer/terms.html'
    context = {
    }
    return render(request, template, context)


href = 'http://directpr.herokuapp.com'


def getCode(request):
    return HttpResponseRedirect(
        'http://oauth.vk.com/authorize?client_id=' + settings.VK_APP_ID +
        '&redirect_uri=' + href +
        '/consumer/vk/processCode/&response_type=code&scope=wall+offline')


def processCode(request):
    try:
        us = Consumer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

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
        return HttpResponseRedirect('/')

    r = postVK(u)

    template = 'consumer/text.html'
    context = {
        "text": r,
    }
    return render(request, template, context)


def campaniesMain(request):
    try:
        u = Consumer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    template = 'consumer/campaniesMain.html'
    context = {
        "id": u.pk,
    }
    return render(request, template, context)


def campanies(request, tp):
    try:
        us = Consumer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    # не участвует
    if tp == '0':
        print("Неактивные")
        campanies = []
        for c in ConsumerMarketCamp.objects.filter(consumer=us).filter(joinType=1):
            t = c.marketCamp
            campanies.append(
                {"viewPrice": t.viewPrice,
                 "platform": MarketCamp.platforms[t.platform],
                 "cid": t.id, "viewCnt": t.curViewCnt,
                 "startTime": t.startTime.strftime("%d.%m.%y"),
                 "endTime": t.endTime.strftime("%d.%m.%y"),
                 "image": t.image,
                 })
        template = 'consumer/m_campanies.html'
        context = {
            'campanies': campanies,
            'caption': "Неактивные рекламные кампании"
        }
        return render(request, template, context)
    # участвует
    elif tp == '1':
        print("Активные")
        campanies = []
        for c in ConsumerMarketCamp.objects.filter(consumer=us, joinType=1):
            t = c.marketCamp
            campanies.append(
                {"viewPrice": t.viewPrice,
                 "platform": MarketCamp.platforms[t.platform],
                 "cid": t.id, "viewCnt": t.curViewCnt,
                 "startTime": t.startTime.strftime("%d.%m.%y"),
                 "endTime": t.endTime.strftime("%d.%m.%y"),
                 "image": t.image,
                 })
        template = 'consumer/m_campanies.html'
        context = {
            'campanies': campanies,
            'caption': "Активные рекламные кампании"
        }
        return render(request, template, context)
    # участвовал
    elif tp == '2':
        return HttpResponseRedirect('/consumer/campanies/')


def detailCampany(request, tid):
    m = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins") or (is_member(request.user, "consumers"))):
        return HttpResponseRedirect('/')

    try:
        us = Consumer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    try:
        cm = ConsumerMarketCamp.objects.get(marketCamp=m, consumer=us)
        state = ConsumerMarketCamp.joinTypes[cm.joinType]
        viewCnt = cm.viewCnt
    except:
        state = 0
        viewCnt = 0

    context = {
        "m": m,
        "id": tid,
        "state": state,
        "viewCnt": viewCnt,
    }
    return render(request, 'consumer/detail_campany.html', context)


def process(request):
    if not (is_member(request.user, "admins") or is_member(request.user, "consumers")):
        return HttpResponseRedirect('/')

    try:
        u = Consumer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    for c in ConsumerMarketCamp.objects.all():
        id = c.consumer.vk_id
        post_id = c.postId
        cnt = getViewCnt(id, post_id, c.consumer.vk_token)
        c.viewCnt = cnt
        c.save()

    reposts_cms = getRepostedCompanies(u.vk_id, u.vk_token)

    print(reposts_cms)
    for m in MarketCamp.objects.all():
        for r in reposts_cms:
            if m == r["m"]:
                print("reposted")
                try:
                    cm = ConsumerMarketCamp.objects.get(marketCamp=m, consumer=u)
                    print("Есть репост, есть компания")
                except:
                    cm = ConsumerMarketCamp.objects.create(marketCamp=m, consumer=u, joinType=1, postId=r["id"],
                                                           link="https://vk.com/wall" + str(u.vk_id) + "_" + str(
                                                               r["id"]))
                    print("Есть репост, нет компании")
                    cm.save()
            else:
                print("not reposted")
                try:
                    cm = ConsumerMarketCamp.objects.get(marketCamp=m, consumer=u, joinType=1)
                    leaveCampany(cm)
                except:
                    pass

    return HttpResponseRedirect('/consumer/campanies/')
