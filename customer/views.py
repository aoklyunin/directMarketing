from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from consumer.models import ConsumerMarketCamp
from customer.forms import MarketCampForm
from customer.models import Customer, ReplenishTransaction, MarketCamp
from mainApp.code import is_member
from mainApp.forms import CustomerForm, PaymentForm, TextForm, CommentForm
from mainApp.models import Comment
from mainApp.views import getErrorPage


def customerError(request):
    return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только администраторам и заказчикам')

def customerOnlyError(request):
    return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только заказчикам')

def autorizedOnlyError(request):
    return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только авторизованным пользоавтелям')


def index(request):
    if not request.user.is_authenticated:
        return autorizedOnlyError(request)
    try:
        us = Customer.objects.get(user=request.user)
    except:
        return getErrorPage(request, 'Ошибка заказчика', 'Пользователь не является заказчиком')

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
        return autorizedOnlyError(request)

    try:
        u = Customer.objects.get(user=request.user)
    except:
        return getErrorPage(request, 'Ошибка заказчика', 'Пользователь не является заказчиком')

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
    cms = MarketCamp.objects.all().order_by('startTime')

    if not (is_member(request.user, "admins") or is_member(request.user, "customers")):
        return customerError(request)

    campanies = []
    for t in cms:
        campanies.append(
            {"viewPrice": t.viewPrice, "targetViewCnt": t.targetViewCnt,
             "platform": MarketCamp.platforms[t.platform],
             "cid": t.id, 'curViewCnt': t.curViewCnt, "isActive": t.isActive,
             "startTime": t.startTime.strftime("%d.%m.%y"),
             "endTime": t.endTime.strftime("%d.%m.%y"),
             "adminApproved": t.adminApproved,
             })

    template = 'customer/campanies.html'
    context = {
        'campanies': campanies,
        'caption': "Рекламные кампании"
    }
    return render(request, template, context)


def startCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return customerError(request)


    if (not ((mc.curViewCnt >= mc.targetViewCnt) or (mc.customer.balance < mc.budget))) and mc.adminApproved:
        mc.customer.balance -= mc.budget
        mc.isActive = True
        mc.save()
        mc.customer.save()

    return HttpResponseRedirect('/customer/campanies/')


def stopCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return customerError(request)

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
        return getErrorPage(request, 'Ошибка заказчика', 'Пользователь не является заказчиком')

    cm = MarketCamp.objects.create(customer=u)

    return HttpResponseRedirect('/customer/campany/detail/' + str(cm.pk) + "/")


def replenish(request):
    try:
        u = Customer.objects.get(user=request.user)
    except:
        return getErrorPage(request, 'Ошибка заказчика', 'Пользователь не является заказчиком')

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
    ct = ReplenishTransaction.objects.get(id=int(tid))
    if request.method == 'POST':
        try:
            cf = CommentForm(request.POST)
            if cf.is_valid():
                c = Comment.objects.create(dt=cf.cleaned_data["dt"], author=request.user,
                                           text=cf.cleaned_data["value"])
                ct.comments.add(c)
            return HttpResponse("ye")
        except:
            return HttpResponse("no")

    if not (is_member(request.user, "admins") or request.user == ct.customer.user):
        return customerError(request)

    # ("-date")
    comments = []
    for c in ct.comments.order_by('-dt')[:6]:
        comments.append({"text": c.text.replace("\n", " "), "isUsers": "false" if c.author == request.user else "true",
                         "name": c.author.first_name, "date": c.dt.strftime("%H:%M")})

    comments = list(reversed(comments))

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
        "caption": "Заявка на внесение средств №" + str(tid),
        "state_val": ReplenishTransaction.states[ct.state],
        "state": ct.state,
        "comments": comments,
        "from_av": from_av,
        "to_av": to_av,
        "target": "/customer/replenish/detail/"+tid+"/",
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
        return getErrorPage(request, 'Ошибка заказчика', 'Пользователь не является заказчиком')


def campamy_discuss(request, tid):
    ct = MarketCamp.objects.get(id=tid)
    if not (is_member(request.user, "admins") or request.user == ct.customer.user):
        return customerError(request)

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


def modifyCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)
    print("modify")

    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return customerError(request)

    isAdmin = is_member(request.user, "admins")
    print(isAdmin)
    if request.method == 'POST':
        # строим форму на основе запроса
        form = MarketCampForm(request.POST, request.FILES)
        # если форма заполнена корректно
        if form.is_valid():
            mc.description = form.cleaned_data['description']
            mc.description = form.cleaned_data['description']
            mc.viewPrice = form.cleaned_data['viewPrice']
            mc.budget = form.cleaned_data['budget']
            mc.targetViewCnt = mc.budget / mc.viewPrice
            mc.platform = int(form.cleaned_data['platform'])
            if isAdmin:
                mc.adminApproved = MarketCamp.STATE_APPROVED
                mc.vkPostID = form.cleaned_data['vkPostID']
            else:
                mc.adminApproved = MarketCamp.STATE_PROCESS
                if form.cleaned_data['image'] != "template.jpg":
                    mc.image = form.cleaned_data['image']
            mc.save()

            return HttpResponseRedirect('/customer/campanies/')


def detailCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return customerError(request)

    form = MarketCampForm(instance=mc)
    form.fields["platform"].initial = mc.platform
    form.fields["image"].initial = None

    template = 'customer/detail_campany.html'
    context = {
        "form": form,
        "isAdmin": is_member(request.user, "admins"),
        "caption": "Маркетинговая кампания №" + str(tid),
        "id": tid,
        "link": "https://vk.com/wall"+str(MarketCamp.group_id)+"_"+str(mc.vkPostID),
        "disableModify": mc.isActive,
    }
    return render(request, template, context)


a = '''def detailCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)
    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        try:
            cf = CommentForm(request.POST)
            if cf.is_valid():
                c = Comment.objects.create(dt=cf.cleaned_data["dt"], author=request.user,
                                           text=cf.cleaned_data["value"])
                ct.comments.add(c)
            return HttpResponse("ye")
        except:
            return HttpResponse("no")

    if not (is_member(request.user, "admins") or request.user == ct.customer.user):
        return HttpResponseRedirect('/')

    # ("-date")
    comments = []
    for c in ct.comments.order_by('-dt')[:6]:
        comments.append({"text": c.text.replace("\n", " "), "isUsers": "false" if c.author == request.user else "true",
                         "name": c.author.first_name, "date": c.dt.strftime("%H:%M")})

    comments = list(reversed(comments))

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
        "caption": "Заявка на внесение средств №" + str(tid),
        "state_val": ReplenishTransaction.states[ct.state],
        "state": ct.state,
        "comments": comments,
        "from_av": from_av,
        "to_av": to_av,
        "target": "/customer/replenish/detail/"+tid+"/",
    }
    return render(request, template, context)
'''