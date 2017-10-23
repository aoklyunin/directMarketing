import json

import requests
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.

from consumer.form import ConsumerForm
from consumer.localCode import postVK
from consumer.models import Consumer, WithdrawTransaction
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
        r = requests.get('https://api.vk.com/method/users.get?user_ids=' + str(us.vk_id)).json()
        uid = r['response']['uid']
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


def campanies(request, tp):
    if not (is_member(request.user, "customers")):
        return HttpResponseRedirect('/')

    try:
        us = Customer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    cms = MarketCamp.objects.filter(customer=us).order_by('startTime')
    campanies = []
    for t in cms:
        campanies.append(
            {"viewPrice": t.viewPrice, "targetViewCnt": t.targetViewCnt,
             "platform": MarketCamp.platforms[t.platform],
             "cid": t.id, 'curViewCnt': t.curViewCnt, "isActive": t.isActive,
             "startTime": t.startTime.strftime("%d.%m.%y"),
             "endTime": t.endTime.strftime("%d.%m.%y"),
             "image": t.image,
             "adminApproved": t.adminApproved,
             "canNotActivate": (t.curViewCnt >= t.targetViewCnt) or (us.balance < t.budget),
             })

    template = 'customer/campanies.html'
    context = {
        'campanies': campanies,
        'caption': "Рекламные кампании"
    }
    return render(request, template, context)


def detailCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = MarketCampForm(request.POST, request.FILES)
        # если форма заполнена корректно
        if form.is_valid():
            if form.cleaned_data['image'] != "template.jpg":
                mc.image = form.cleaned_data['image']
            mc.description = form.cleaned_data['description']
            mc.viewPrice = form.cleaned_data['viewPrice']
            mc.budget = form.cleaned_data['budget']
            mc.targetViewCnt = mc.budget / mc.viewPrice
            mc.platform = int(form.cleaned_data['platform'])
            mc.adminApproved = False
            mc.save()
            return HttpResponseRedirect('/customer/campanies/')

    form = MarketCampForm(instance=mc)
    form.fields["platform"].initial = mc.platform
    form.fields["image"].initial = None

    template = 'customer/detail_campany.html'
    context = {
        "form": form,
        "id": tid,
        "disableModify": mc.isActive,
    }
    return render(request, template, context)


def joinCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return HttpResponseRedirect('/')

    if (not ((mc.curViewCnt >= mc.targetViewCnt) or (mc.customer.balance < mc.budget))) and mc.adminApproved:
        mc.customer.balance -= mc.budget
        mc.isActive = True
        mc.save()
        mc.customer.save()

    return HttpResponseRedirect('/customer/campanies/')


def leaveCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return HttpResponseRedirect('/')

    mc.budget = mc.budget - mc.curViewCnt * mc.viewPrice
    mc.targetViewCnt -= mc.curViewCnt
    mc.customer.balance += mc.budget
    mc.customer.save()
    mc.curViewCnt = 0
    mc.isActive = False
    mc.save()

    return HttpResponseRedirect('/customer/campanies/')


href = 'http://directpr.herokuapp.com'


def getCode(request):
    print("get code called")
    return HttpResponseRedirect(
        'http://oauth.vk.com/authorize?client_id=' + settings.VK_APP_ID +
        '&redirect_uri=' + href +
        '/consumer/vk/processCode/&response_type=code&scope=wall')


def processCode(request):
    print("processCode called")
    print(request.GET)
    code = request.GET["code"]
    print(code)
    r = requests.get('https://oauth.vk.com/access_token?client_id=' + settings.VK_APP_ID +
                     '&client_secret=' + settings.VK_API_SECRET + '&redirect_uri=' + href +
                     '/consumer/vk/processCode/&code=' + code).json()

    template = 'customer/vkSaveToken.html'
    context = {
        'token': r["access_token"],
        'uid': r["user_id"],
        'expires_in': r["expires_in"],
    }
    return render(request, template, context)


def postVKview(request):
    try:
        u = Consumer.objects.get(user=request.user)

    except:
        return HttpResponseRedirect('/')

    postVK(u)

    return HttpResponseRedirect('/consumer/')
