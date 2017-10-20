from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from consumer.models import Consumer
from customer.forms import MarketCampForm
from customer.models import Customer, ReplenishTransaction, MarketCamp
from mainApp.code import is_member
from mainApp.forms import CustomerForm, PaymentForm, TextForm, ConsumerForm
from mainApp.models import Comment


def index(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect('/')

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
            us.save()

    form = ConsumerForm(initial={'name': us.user.first_name, 'second_name': us.user.last_name,
                                 'qiwi': us.qiwi})
    template = 'consumer/index.html'

    context = {
        "u": us,
        "form": form,
    }
    return render(request, template, context)


def balance(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    try:
        u = Customer.objects.get(user=request.user)
    except:
       return  HttpResponseRedirect('/')

    ts = ReplenishTransaction.objects.filter(customer=u).order_by('dt')
    transactions = []
    for t in ts:
        transactions.append({"date": t.dt, "value": t.value, "state": ReplenishTransaction.states[t.state],
                             "tid": t.id})
    template = 'customer/balance.html'
    context = {
        "u": u,
        "transactions": transactions,
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


def leaveCamapany(request, tid):
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


def withdraw(request):
    try:
        u = Customer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = PaymentForm(request.POST)
        if form.is_valid():
            t = ReplenishTransaction.objects.create(customer=u, value=form.cleaned_data["value"])
            return HttpResponseRedirect('/customer/replenish_detail/' + str(t.pk) + "/")

    template = 'customer/replenish.html'
    qiwi = "+7 921 583 28 98"
    context = {
        "form": PaymentForm(),
        "qiwi": qiwi,
    }
    return render(request, template, context)


def withdraw_detail(request, tid):
    ct = ReplenishTransaction.objects.get(id=tid)
    if not (is_member(request.user, "admins") or request.user == ct.customer.user):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = TextForm(request.POST)
        if form.is_valid():
            c = Comment.objects.create(author=request.user, text=form.cleaned_data["value"])
            ct.comments.add(c)

    template = 'customer/replenish_detail.html'
    context = {
        "id": tid,
        "need_pay": ct.state == 0,
        "date": ct.dt.strftime("%d.%m.%y"),
        "state": ReplenishTransaction.states[ct.state],
        "comments": ct.comments.order_by('dt'),
        "form": TextForm(),
    }
    return render(request, template, context)


def terms(request):
    template = 'customer/terms.html'
    context = {
    }
    return render(request, template, context)


def withdraw_set_payed(request, tid):
    ct = ReplenishTransaction.objects.get(id=tid)
    if ct.customer.user == request.user:
        ct.state = 1
        ct.save()
        return HttpResponseRedirect('/customer/replenish_detail/' + str(tid) + "/")
    else:
        return HttpResponseRedirect('/')
