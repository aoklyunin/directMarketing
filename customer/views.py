from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from customer.forms import MarketCampForm
from customer.models import Customer, ReplenishTransaction, MarketCamp
from mainApp.code import is_member
from mainApp.forms import CustomerForm, PaymentForm, CommentForm
from mainApp.localCode import genRandomString
from mainApp.models import Comment
from mainApp.views import getErrorPage, autorizedOnlyError, processComment


# ошибка доступа Админ или Заказчик
def customerAdminError(request):
    return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только администраторам и заказчикам')


# ошибка доступа Заказчик
def customerError(request):
    return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только заказчикам')


# главная страница заказчика
def index(request):
    # проверяем, что текущий пользователь - заказчик
    if not request.user.is_authenticated:
        return autorizedOnlyError(request)
    try:
        us = Customer.objects.get(user=request.user)
    except:
        return getErrorPage(request, 'Ошибка заказчика', 'Пользователь не является заказчиком')

    # обрабатываем форму
    if request.method == 'POST':
        # строим форму на основе запроса
        form = CustomerForm(request.POST)
        if form.is_valid():
            us.qiwi = form.cleaned_data['qiwi']
            us.companyName = form.cleaned_data['name']
            us.save()

    # получаем заявки на внесение у текущего пользователя
    rts = ReplenishTransaction.objects.filter(customer=us).order_by('-dt')[:7]
    transactions = []
    for t in rts:
        if t.state == 0:
            stateClass = "text-muted"
        elif t.state == 1:
            stateClass = "text-info"
        elif t.state == 2:
            stateClass = "text-danger"
        elif t.state == 3:
            stateClass = "text-success"
        else:
            stateClass = ""

        transactions.append(
            {"date": t.dt.strftime("%d.%m"), "value": t.value, "stateClass": stateClass,
             "state": ReplenishTransaction.states[t.state],
             "tid": t.id, "notReadedCnt": t.comments.exclude(author=t.customer.user).filter(readed=False).count()})
    # передаём форму для изменения данных
    form = CustomerForm(initial={'name': us.companyName, 'qiwi': us.qiwi})
    template = 'customer/index.html'

    context = {
        "u": us,
        "form": form,
        "transactions": transactions,
        "caption": "Профиль пользователя",
    }
    return render(request, template, context)


# список кампаний
def campanies(request):
    # проверяем, что пользователь - админ или заказчик этой маркетинговой кампании
    if is_member(request.user, "admins"):
        cms = MarketCamp.objects.all().order_by('startTime')
    elif is_member(request.user, "customers"):
        try:
            us = Customer.objects.get(user=request.user)
            cms = MarketCamp.objects.filter(customer=us).order_by('startTime')
        except:
            return customerError(request)
    else:
        return customerAdminError(request)

    # получаем список кампаний
    campanies = []
    for t in cms:
        if request.user == t.customer.user:
            commentCnt = t.comments.exclude(author=t.customer.user).filter(readed=False).count()
        else:
            commentCnt = t.comments.filter(author=t.customer.user, readed=False).count()

        campanies.append(
            {"viewPrice": t.viewPrice, "targetViewCnt": t.targetViewCnt,
             "platform": MarketCamp.platforms[t.platform],
             "cid": t.id, 'curViewCnt': t.curViewCnt, "isActive": t.isActive,
             "startTime": t.startTime.strftime("%d.%m.%y"),
             "endTime": t.endTime.strftime("%d.%m.%y"),
             "adminApproved": t.adminApproved,
             "notReadedCnt": commentCnt,
             })

    template = 'customer/campanies.html'
    context = {
        'campanies': campanies,
        'caption': "Рекламные кампании"
    }
    return render(request, template, context)


# запуск кампании
def startCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)
    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return customerAdminError(request)
    # Если набранное число просмотров меньше желаемого, баланс позволяет и админ одобрил
    if (mc.curViewCnt < mc.targetViewCnt) and \
            (mc.customer.balance >= mc.budget) and (mc.adminApproved):
        # вычетаем бюджет кампании из баланса
        mc.customer.balance -= mc.budget
        mc.isActive = True
        mc.save()
        mc.customer.save()

    return HttpResponseRedirect('/customer/campanies/')


# остановить кампанию
def stopCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return customerAdminError(request)

    # если кампания активна
    if not mc.isActive:
        # вычетаем из бюджета оплаченные просмотры
        mc.budget = mc.budget - mc.curViewCnt * mc.viewPrice
        # вычетаем из желаемого кол-ва просмотров выполненое
        mc.targetViewCnt -= mc.curViewCnt
        # возвращаем на баланс пользователя неизрасходованный бюджет
        mc.customer.balance += mc.budget
        mc.customer.save()
        # обнуляем текущее число просмотров
        mc.curViewCnt = 0
        # делаем кампанию неактивной
        mc.isActive = False
        mc.save()

    return HttpResponseRedirect('/customer/campanies/')


# создаём кампанию
def createCampany(request):
    try:
        u = Customer.objects.get(user=request.user)
    except:
        return customerError(request)

    cm = MarketCamp.objects.create(customer=u)
    return HttpResponseRedirect('/customer/campany/detail/' + str(cm.pk) + "/")


# внесение средств
def replenish(request):
    try:
        u = Customer.objects.get(user=request.user)
    except:
        return getErrorPage(request, 'Ошибка заказчика', 'Пользователь не является заказчиком')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = PaymentForm(request.POST)
        if form.is_valid():
            t = ReplenishTransaction.objects.create(customer=u, value=form.cleaned_data["value"], paymentComment=form.cleaned_data["comment"])
            return HttpResponseRedirect('/customer/replenish/detail/' + str(t.pk) + "/")

    template = 'customer/replenish.html'
    qiwi = "+7 921 583 28 98"
    context = {
        "form": PaymentForm(initial={"comment": genRandomString(6)}),
        "qiwi": qiwi,
        "caption": "Пополнение баланса"
    }
    return render(request, template, context)


# детали заявки на внесение
def replenish_detail(request, tid):
    rt = ReplenishTransaction.objects.get(id=int(tid))
    # обработка нового комментария
    if request.method == 'POST':
        return processComment(request, rt)

    if not (is_member(request.user, "admins") or request.user == rt.customer.user):
        return customerAdminError(request)

    if request.user == rt.customer.user:
        rt.comments.exclude(author=rt.customer.user).filter(readed=False).update(readed=True)
    else:
        rt.comments.filter(author=rt.customer.user, readed=False).update(readed=True)

    # получаем последние 6 комментариев
    comments = []
    for c in rt.comments.order_by('-dt')[:6]:
        comments.append({"text": c.text.replace("\n", " "), "isUsers": "false" if c.author == request.user else "true",
                         "name": c.author.first_name, "date": c.dt.strftime("%H:%M")})
    comments = list(reversed(comments))

    # получаем картинки для чата
    if request.user == rt.customer.user:
        from_av = "images/customer_avatar.jpg"
        to_av = "images/admin_avatar.jpg"
    else:
        from_av = "images/admin_avatar.jpg"
        to_av = "images/customer_avatar.jpg"

    template = 'customer/replenish_detail.html'
    context = {
        "id": tid,
        "need_pay": rt.state == 0,
        "caption": "Заявка на внесение средств №" + str(tid),
        "state_val": ReplenishTransaction.states[rt.state],
        "state": rt.state,
        "value": rt.value,
        "comment": rt.paymentComment,
        "qiwi": "+7 921 583 28 98",
        "comments": comments,
        "from_av": from_av,
        "to_av": to_av,
        "isUser": request.user == rt.customer.user,
        "target": "/customer/replenish/detail/" + tid + "/",
    }
    return render(request, template, context)


# заказчик говорит, что заявка оплачена
def replenish_set_payed(request, tid):
    ct = ReplenishTransaction.objects.get(id=tid)
    if ct.customer.user == request.user:
        ct.state = 1
        ct.save()
        return HttpResponseRedirect('/customer/replenish/detail/' + str(tid) + "/")
    else:
        return getErrorPage(request, 'Ошибка заказчика', 'Пользователь не является заказчиком')


# изменить маркетинговую кампанию
def modifyCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)
    # если пользователь не админ и не заказчик этой кампании
    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return customerAdminError(request)

    # является ли пользователь админом
    isAdmin = is_member(request.user, "admins")
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
            # если пользователь - админ
            if isAdmin:
                # говорим, что кампания проверена
                mc.adminApproved = MarketCamp.STATE_APPROVED
                # сохраняем id записи в группе
                mc.vkPostID = form.cleaned_data['vkPostID']
            else:
                # говорим, что кампания не проверена
                mc.adminApproved = MarketCamp.STATE_PROCESS
                # если картинка - новая
                if form.cleaned_data['image'] != "template.jpg":
                    mc.image = form.cleaned_data['image']
            mc.save()

            return HttpResponseRedirect('/customer/campanies/')

    # если было просто обращение к этой странице
    return getErrorPage(request, 'Ошибка запроса', 'Эта страница предназначена только для post-запросов')


# детали кампании
def detailCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)
    # если пользователь не админ и не заказчик этой кампании
    if not (is_member(request.user, "admins") or request.user == mc.customer.user):
        return customerAdminError(request)

    # обработка комментария
    if request.method == 'POST':
        return processComment(request, mc)

    # форма изменения кампании
    form = MarketCampForm(instance=mc)
    form.fields["platform"].initial = mc.platform
    form.fields["image"].initial = None

    if request.user == mc.customer.user:
        mc.comments.exclude(author=mc.customer.user).filter(readed=False).update(readed=True)
    else:
        mc.comments.filter(author=mc.customer.user, readed=False).update(readed=True)

    # получаем комментарии
    comments = []
    for c in mc.comments.order_by('-dt')[:6]:
        comments.append({"text": c.text.replace("\n", " "), "isUsers": "false" if c.author == request.user else "true",
                         "name": c.author.first_name, "date": c.dt.strftime("%H:%M")})
    comments = list(reversed(comments))

    # получаем картинку для чата
    if request.user == mc.customer.user:
        from_av = "images/customer_avatar.jpg"
        to_av = "images/admin_avatar.jpg"
    else:
        from_av = "images/admin_avatar.jpg"
        to_av = "images/customer_avatar.jpg"

    template = 'customer/campany_detail.html'
    context = {
        "form": form,
        "isAdmin": is_member(request.user, "admins"),
        "caption": "Маркетинговая кампания №" + str(tid),
        "id": tid,
        "link": "https://vk.com/wall" + str(MarketCamp.group_id) + "_" + str(mc.vkPostID),
        "disableModify": mc.isActive,
        "comments": comments,
        "from_av": from_av,
        "to_av": to_av,
        "target": "/customer/campany/detail/" + tid + "/",

    }
    return render(request, template, context)
