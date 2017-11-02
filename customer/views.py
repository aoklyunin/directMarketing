from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from consumer.models import ConsumerMarketCamp
from customer.forms import MarketCampForm
from customer.models import Customer, ReplenishTransaction, MarketCamp
from mainApp.code import is_member
from mainApp.forms import CustomerForm, PaymentForm, TextForm
from mainApp.models import Comment


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    try:
        us = Customer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = CustomerForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            us.qiwi = form.cleaned_data['qiwi']
            us.companyName = form.cleaned_data['name']
            us.save()

    form = CustomerForm(initial={'name': us.companyName, 'qiwi': us.qiwi})
    template = 'customer/index.html'

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
        return HttpResponseRedirect('/')

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


def campanies(request):
    if not (is_member(request.user, "customers")):
        return HttpResponseRedirect('/')

    try:
        us = Customer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    cms = MarketCamp.objects.filter(customer=us).order_by('startTime')
    campanies = []
    for t in cms:
        if t.isActive:
            t.curViewCnt = 0

            for c in ConsumerMarketCamp.objects.filter(marketCamp=t, joinType=1):
                t.curViewCnt += c.viewCnt
                t.save()

            if t.curViewCnt >= t.targetViewCnt:
                t.isActive = False
                t.save()

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


def startCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return HttpResponseRedirect('/')

    if (not ((mc.curViewCnt >= mc.targetViewCnt) or (mc.customer.balance < mc.budget))) and mc.adminApproved:
        mc.customer.balance -= mc.budget
        mc.isActive = True
        mc.save()
        mc.customer.save()

    return HttpResponseRedirect('/customer/campanies/')


def stopCampany(request, tid):
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


def createCampany(request):
    try:
        u = Customer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')
    cm = MarketCamp.objects.create(customer=u)

    return HttpResponseRedirect('/customer/campany/detail/' + str(cm.pk) + "/")


def replenish(request):
    try:
        u = Customer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = PaymentForm(request.POST)
        if form.is_valid():
            t = ReplenishTransaction.objects.create(customer=u, value=form.cleaned_data["value"])
            return HttpResponseRedirect('/customer/replenish/detail/' + str(t.pk) + "/")

    template = 'customer/replenish.html'
    qiwi = "+7 921 583 28 98"
    context = {
        "form": PaymentForm(),
        "qiwi": qiwi,
    }
    return render(request, template, context)


def replenish_detail(request, tid):
    print("detail called")
    ct = ReplenishTransaction.objects.get(id=tid)
    if request.method == 'POST':
        print("post")
        try:
            tf = TextForm(request.POST)
            if tf.is_valid():
                c = Comment.objects.create(author=request.user, text=tf.cleaned_data["value"])
                ct.comments.add(c)
            return "ye"
        except:
            return "no"

    if not (is_member(request.user, "admins") or request.user == ct.customer.user):
        return HttpResponseRedirect('/')

    comments = []
    for c in ct.comments.order_by('dt'):
        comments.append({"text": c.text, "isUsers": "false" if c.author == request.user else "true",
                         "name": c.author.first_name, "date": c.dt.strftime("%I:%M")})

    if request.user == ct.customer.user:
        from_av = "images/customer_avatar.jpg"
        to_av = "images/admin_avatar.jpg"
    else:
        from_av = "images/admin_avatar.jpg"
        to_av = "images/customer_avatar.jpg"

    template = 'customer/replenish_detail.html'
    context = {
        "id": tid,
        "need_pay": ct.state == 0,
        "caption": "Заявка на вывод средств №" + str(tid),
        "state_val": ReplenishTransaction.states[ct.state],
        "state": ct.state,
        "comments": comments,
        "from_av":  from_av,
        "to_av":  to_av,
    }
    return render(request, template, context)


def terms(request):
    template = 'customer/terms.html'
    context = {
    }
    return render(request, template, context)


def replenish_set_payed(request, tid):
    ct = ReplenishTransaction.objects.get(id=tid)
    if ct.customer.user == request.user:
        ct.state = 1
        ct.save()
        return HttpResponseRedirect('/customer/replenish/detail/' + str(tid) + "/")
    else:
        return HttpResponseRedirect('/')


def campamy_discuss(request, tid):
    ct = MarketCamp.objects.get(id=tid)
    if not (is_member(request.user, "admins") or request.user == ct.customer.user):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = TextForm(request.POST)
        if form.is_valid():
            c = Comment.objects.create(author=request.user, text=form.cleaned_data["value"])
            ct.comments.add(c)

    template = 'customer/campany_discuss.html'
    context = {
        "comments": ct.comments.order_by('dt'),
        "id": tid,
    }
    return render(request, template, context)
