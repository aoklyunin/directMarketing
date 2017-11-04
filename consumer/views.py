import json

import requests
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.

from consumer.form import ConsumerForm
from consumer.localCode import postVK, getReposts, leaveCampany, getRepostedCompanies, getViewCnt, \
    getNotRepostedCompanies
from consumer.models import Consumer, WithdrawTransaction, ConsumerMarketCamp
from customer.models import Customer, ReplenishTransaction, MarketCamp
from mainApp.code import is_member
from mainApp.forms import PaymentForm, TextForm, CommentForm
from mainApp.models import Comment
from mysite import settings


def withdraw_detail(request, tid):
    ct = WithdrawTransaction.objects.get(id=int(tid))

    if not (is_member(request.user, "admins") or request.user == ct.consumer.user):
        return HttpResponseRedirect('/')

    print("detail called")
    print(tid)

    if request.method == 'POST':
        print("post")
        try:
            print(request.POST)
            cf = CommentForm(request.POST)
            print(cf)
            if cf.is_valid():
                print(cf.cleaned_data["dt"])
                c = Comment.objects.create(dt=cf.cleaned_data["dt"], author=request.user,
                                           text=cf.cleaned_data["value"])
                ct.comments.add(c)
            return HttpResponse("ye")
        except:
            return HttpResponse("no")



    # ("-date")
    comments = []
    for c in ct.comments.order_by('-dt')[:6]:
        print(c.dt.strftime("%H:%M") + ": " + c.text)
        comments.append({"text": c.text.replace("\n", " "), "isUsers": "false" if c.author == request.user else "true",
                         "name": c.author.first_name, "date": c.dt.strftime("%H:%M")})

    comments = list(reversed(comments))

    if request.user == ct.consumer.user:
        from_av = "images/consumer_avatar.jpg"
        to_av = "images/admin_avatar.jpg"
    else:
        from_av = "images/admin_avatar.jpg"
        to_av = "images/consumer_avatar.jpg"

    template = 'consumer/withdraw_detail.html'
    context = {
        "id": tid,
        "need_pay": ct.state == 0,
        "caption": "Заявка на вывод средств №" + str(tid),
        "state_val": WithdrawTransaction.states[ct.state],
        "state": ct.state,
        "comments": comments,
        "from_av": from_av,
        "to_av": to_av,
        "target": "/consumer/withdraw/detail/"+tid+"/",
    }
    return render(request, template, context)



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
        for m in MarketCamp.objects.filter(isActive=True):
            try:
                ConsumerMarketCamp.objects.get(consumer=us, marketCamp=m)
            except:
                campanies.append(
                    {"viewPrice": m.viewPrice,
                     "platform": MarketCamp.platforms[m.platform],
                     "cid": m.id, "viewCnt": m.curViewCnt,
                     "startTime": m.startTime.strftime("%d.%m.%y"),
                     "endTime": m.endTime.strftime("%d.%m.%y"),
                     "image": m.image,
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
                 "cid": t.id, "viewCnt": c.viewCnt,
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
        print("Участвовал")
        campanies = []
        for c in ConsumerMarketCamp.objects.filter(consumer=us).filter(joinType=2):
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
            'caption': "Участвовал"
        }
        return render(request, template, context)


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
        try:
            id = c.consumer.vk_id
            post_id = c.postId
            cnt = getViewCnt(id, post_id, c.consumer.vk_token)
            c.viewCnt = cnt
            c.save()
        except:
            print("Запись удалена")

    reposted_cms = getRepostedCompanies(u.vk_id, u.vk_token)

    for r in reposted_cms:
        m = r["m"]
        if m.isActive:
            try:
                cm = ConsumerMarketCamp.objects.get(marketCamp=m, consumer=u)
                print("Есть репост, есть компания")
            except:
                cm = ConsumerMarketCamp.objects.create(marketCamp=m, consumer=u, joinType=1, postId=r["id"],
                                                       link="https://vk.com/wall" + str(u.vk_id) + "_" + str(
                                                           r["id"]))

                id = cm.consumer.vk_id
                post_id = cm.postId
                cnt = getViewCnt(id, post_id, cm.consumer.vk_token)
                cm.viewCnt = cnt
                cm.save()

                print("Есть репост, нет компании")
        else:
            try:
                cm = ConsumerMarketCamp.objects.get(marketCamp=m, consumer=u, joinType=1)
                leaveCampany(cm)
                print("Есть репост, есть неактивная компания ")
            except:
                pass

    not_reposted_cms = getNotRepostedCompanies(reposted_cms)

    for r in not_reposted_cms:
        m = r["m"]
        try:
            cm = ConsumerMarketCamp.objects.get(marketCamp=m, consumer=u, joinType=1, postId=r["id"])
            leaveCampany(cm)
        except:
            pass

    return HttpResponseRedirect('/consumer/campanies/')
