import requests
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from consumer.form import ConsumerForm
from consumer.localCode import postVK, leaveCampany, getRepostedCompanies, getViewCnt, \
    getNotRepostedCompanies
from consumer.models import Consumer, WithdrawTransaction, ConsumerMarketCamp
from customer.models import MarketCamp
from mainApp.code import is_member
from mainApp.forms import PaymentForm, CommentForm
from mainApp.models import Comment
from mainApp.views import getErrorPage, processComment, autorizedOnlyError


# ошибка доступа Админ или Исполнитель
def consumerAdminError(request):
    return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только администраторам и исполнителям')


# ошибка доступа Исполнитель
def consumerError(request):
    return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только исполнителям')


# детали заявки на вывод
def withdrawDetail(request, tid):
    wt = WithdrawTransaction.objects.get(id=int(tid))
    # если не исполнитель и не админ
    if not (is_member(request.user, "admins") or request.user == wt.consumer.user):
        return consumerAdminError(request)

    if request.method == 'POST':
        processComment(request, wt)

    if request.user == wt.consumer.user:
        wt.comments.exclude(author=wt.consumer.user).filter(readed=False).update(readed=True)
    else:
        wt.comments.filter(author=wt.consumer.user, readed=False).update(readed=True)

    # получаем последние шесть коммментариев
    comments = []
    for c in wt.comments.order_by('-dt')[:6]:
        comments.append({"text": c.text.replace("\n", " "), "isUsers": "false" if c.author == request.user else "true",
                         "name": c.author.first_name, "date": c.dt.strftime("%H:%M")})
    comments = list(reversed(comments))

    # получаем картинки для чата
    if request.user == wt.consumer.user:
        from_av = "images/consumer_avatar.jpg"
        to_av = "images/admin_avatar.jpg"
    else:
        from_av = "images/admin_avatar.jpg"
        to_av = "images/consumer_avatar.jpg"

    template = 'consumer/withdraw_detail.html'
    context = {
        "id": tid,
        "caption": "Заявка на вывод средств №" + str(tid),
        "state_val": WithdrawTransaction.states[wt.state],
        "state": wt.state,
        "comments": comments,
        "from_av": from_av,
        "value": wt.value,
        "to_av": to_av,
        "qiwi": wt.consumer.qiwi,
        "target": "/consumer/withdraw/detail/" + tid + "/",
    }
    return render(request, template, context)


# главная страница исполнителя
def index(request):
    # проверяем, что текущий пользователь - исполнитель
    if not request.user.is_authenticated:
        return autorizedOnlyError(request)
    try:
        us = Consumer.objects.get(user=request.user)
    except:
        return getErrorPage(request, 'Ошибка заказчика', 'Пользователь не является исполнителем')

    # обрабатываем форму
    if request.method == 'POST':
        # строим форму на основе запроса
        form = ConsumerForm(request.POST)
        if form.is_valid():
            us.qiwi = form.cleaned_data['qiwi']
            us.user.first_name = form.cleaned_data['name']
            us.user.last_name = form.cleaned_data['second_name']
            us.save()


    # получаем заявки на внесение у текущего пользователя
    rts = WithdrawTransaction.objects.filter(consumer=us).order_by('-dt')
    transactions = []
    for t in rts:
        transactions.append(
            {"date": t.dt.strftime("%d.%m %H:%M"), "value": t.value, "state": WithdrawTransaction.states[t.state],
             "tid": t.id, "notReadedCnt": t.comments.exclude(author=t.consumer.user).filter(readed=False).count()})

    # передаём форму для изменения данных
    form = ConsumerForm(initial={'name': us.user.first_name, 'second_name': us.user.last_name, 'qiwi': us.qiwi})
    template = 'consumer/index.html'

    context = {
        "u": us,
        "form": form,
        "transactions": transactions,
        "caption": "Профиль пользователя",
    }
    return render(request, template, context)


# сформировать заявку
def withdraw(request):
    try:
        u = Consumer.objects.get(user=request.user)
    except:
        return consumerError(request)

    # обработка формы
    if request.method == 'POST':
        # строим форму на основе запроса
        form = PaymentForm(request.POST)
        if form.is_valid():
            t = WithdrawTransaction.objects.create(consumer=u, value=form.cleaned_data["value"])
            t.save()
            return HttpResponseRedirect('/consumer/balance/')

    template = 'consumer/withdraw.html'
    context = {
        "form": PaymentForm(),
        "caption": "Заявка на вывод средств"
    }
    return render(request, template, context)


# страница кампаний
def campanies(request):
    if not (is_member(request.user, "admins") or is_member(request.user, "consumers")):
        return consumerAdminError(request)

    u = Consumer.objects.get(user=request.user)

    template = 'consumer/campanies.html'
    context = {
        "id": u.pk,
        "caption": "Рекламные кампании"
    }
    return render(request, template, context)


# список кампаний
def campaniesList(request, tp):
    try:
        us = Consumer.objects.get(user=request.user)
    except:
        return consumerError(request)

    # не участвует
    if tp == '0':
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
        caption = "Не участвовал"
    # участвует/участвовал
    else:
        campanies = []
        for c in ConsumerMarketCamp.objects.filter(consumer=us, joinType=int(tp)):
            t = c.marketCamp
            campanies.append(
                {"viewPrice": t.viewPrice,
                 "platform": MarketCamp.platforms[t.platform],
                 "cid": t.id, "viewCnt": c.viewCnt,
                 "startTime": t.startTime.strftime("%d.%m.%y"),
                 "endTime": t.endTime.strftime("%d.%m.%y"),
                 "image": t.image,
                 })

        caption = "Активные рекламные кампании" if tp == '1' else "Участвовал"

    template = 'consumer/campanies_list.html'
    context = {
        'campanies': campanies,
        'caption': caption,
    }
    return render(request, template, context)


# детали кампании
def detailCampany(request, tid):
    m = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins") or (is_member(request.user, "consumers"))):
        return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только администраторам и исполнителям')

    try:
        us = Consumer.objects.get(user=request.user)
    except:
        return getErrorPage(request, 'Ошибка поиска', 'Исполнитель не найден')

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
        "platform": MarketCamp.platforms[m.platform],
        "viewCnt": viewCnt,
        "caption": "Рекламная кампания №" + str(m.pk),
        "link": "https://vk.com/wall" + str(MarketCamp.group_id) + "_" + str(m.vkPostID),
    }
    return render(request, 'consumer/campany_detail.html', context)
