from django.http import HttpResponseRedirect
from django.shortcuts import render

from consumer.models import WithdrawTransaction, Consumer, ConsumerMarketCamp
from customer.models import MarketCamp, ReplenishTransaction
from mainApp.code import is_member

# получить страницу ошибки доступа к админской странице
from mainApp.localCode import getFriendsUsers
from mainApp.views import getErrorPage


def adminError(request):
    return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только администраторам')


def dismissCampany(request, tid):
    mc = MarketCamp.objects.get(id=tid)

    if not (is_member(request.user, "admins")):
        return adminError(request)

    mc.adminApproved = MarketCamp.STATE_NOT_APPROVED
    mc.save()

    return HttpResponseRedirect('/customer/campanies/')


# внесение средств
def replenish(request):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    rejectedCnt = 0
    processedCnt = 0
    notProcessedCnt = ReplenishTransaction.objects.filter(state=ReplenishTransaction.STATE_PROCESS).count()

    # Получаем кол-во непрочитанных сообщений
    for rt in ReplenishTransaction.objects.all():
        cnt = rt.comments.filter(author=rt.customer.user, readed=False).count()
        if rt.state == ReplenishTransaction.STATE_PROCESS:
            notProcessedCnt += cnt
        if rt.state == ReplenishTransaction.STATE_ACCEPTED:
            processedCnt += cnt
        if rt.state == ReplenishTransaction.STATE_REJECTED:
            rejectedCnt += cnt

    return render(request,
                  'adminPanel/replenish.html',
                  {"caption": "Панель администратора: внесение",
                   "RejectedCnt": rejectedCnt, "ProcessedCnt": processedCnt, "NotProcessedCnt": notProcessedCnt, })


# отобразить заявки по их состоянию
def replenishList(request, state):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    # получаем состояние заявки
    st = int(state)
    # получаем queryset заявок с таким состоянием
    rt = ReplenishTransaction.objects.filter(state=st).order_by('dt')

    # формируем удобный список для вывода на страницу
    transactions = []
    for t in rt:
        transactions.append({"date": t.dt.strftime("%d.%m.%y"), "value": t.value, "qiwi": t.customer.qiwi,
                             "tid": t.id, "comment": t.paymentComment,
                             "notReadedCnt": t.comments.filter(author=t.customer.user, readed=False).count()})

    return render(request,
                  'adminPanel/replenish_list.html',
                  {"transactions": transactions, "caption": ReplenishTransaction.list_states[st], "state": st})


# Отклонить завку
def replenishReject(request, tid):
    ts = ReplenishTransaction.objects.get(id=tid)

    # если пользователь не админ,
    if not (is_member(request.user, "admins") or ts.customer.user == request.user):
        # переадресация на страницу с ошибкой
        return adminError(request)
    if ts.state == ReplenishTransaction.STATE_WAIT_FOR_PAY or ts.state == ReplenishTransaction.STATE_PROCESS:
        ts.state = ReplenishTransaction.STATE_REJECTED
        ts.save()
    else:
        return getErrorPage(request, "Ошибка отклонения заявки",
                            "Отклонить заявку можно только если она находится в режиме ожидания оплаты или проверки")
    if is_member(request.user, "admins"):
        return HttpResponseRedirect('/adminPanel/replenish/list/1/')
    else:
        return HttpResponseRedirect('/customer/')


# принять заявку
def replenishAccept(request, tid):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    # получаем заявку на вывод
    ts = ReplenishTransaction.objects.get(id=tid)
    if ts.state != ReplenishTransaction.STATE_ACCEPTED:
        c = ts.customer
        c.balance += ts.value
        c.save()
        ts.state = ReplenishTransaction.STATE_ACCEPTED
        ts.save()

    return HttpResponseRedirect('/adminPanel/replenish/list/1/')


# внесение средств
def withdraw(request):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    rejectedCnt = 0
    processedCnt = 0
    notProcessedCnt = WithdrawTransaction.objects.filter(state=WithdrawTransaction.STATE_PROCESS).count()

    # Получаем кол-во непрочитанных сообщений
    for rt in WithdrawTransaction.objects.all():
        cnt = rt.comments.filter(author=rt.consumer.user, readed=False).count()
        if rt.state == WithdrawTransaction.STATE_PROCESS:
            notProcessedCnt += cnt
        if rt.state == WithdrawTransaction.STATE_ACCEPTED:
            processedCnt += cnt
        if rt.state == WithdrawTransaction.STATE_REJECTED:
            rejectedCnt += cnt

    return render(request,
                  'adminPanel/withdraw.html',
                  {"caption": "Панель администратора: вывод",
                   "RejectedCnt": rejectedCnt, "ProcessedCnt": processedCnt, "NotProcessedCnt": notProcessedCnt, })


# отобразить список заявок по состоянию
def withdrawList(request, state):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    # получаем состояние заявки
    st = int(state)
    # получаем queryset заявок с таким состоянием
    wt = WithdrawTransaction.objects.filter(state=st).order_by('dt')

    # формируем удобный список для вывода на страницу
    transactions = []
    for t in wt:
        if not t.consumer.blocked:
            transactions.append({"date": t.dt.strftime("%d.%m.%y"), "value": t.value, "qiwi": t.consumer.qiwi,
                                 "tid": t.id, "canNotPay": t.value > t.consumer.balance, "balance": t.consumer.balance,
                                 "notReadedCnt": t.comments.filter(author=t.consumer.user, readed=False).count()})

    # делаем массив с заголовками для каждого из состояний
    return render(request,
                  'adminPanel/withdraw_list.html',
                  {"transactions": transactions,
                   "caption": WithdrawTransaction.list_states[st], "state": st})


# Отклонить завку
def withdrawReject(request, tid):
    ts = WithdrawTransaction.objects.get(id=tid)

    # если пользователь не админ,
    if not (is_member(request.user, "admins") or ts.consumer.user == request.user):
        # переадресация на страницу с ошибкой
        return adminError(request)

    if ts.state == WithdrawTransaction.STATE_PROCESS:
        ts.consumer.frozenBalance -= ts.value
        ts.consumer.save()
        ts.state = WithdrawTransaction.STATE_REJECTED
        ts.save()
    else:
        return getErrorPage(request, "Ошибка отклонения заявки",
                            "Отклонить заявку можно только если она проверяется")

    if is_member(request.user, "admins"):
        return HttpResponseRedirect('/adminPanel/replenish/list/0/')
    else:
        return HttpResponseRedirect('/consumer/')


# Принять завку
def withdrawAccept(request, tid):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    ct = WithdrawTransaction.objects.get(id=tid)
    if ct.consumer.blocked:
        return getErrorPage(request, "Ошибка вывода средств", "Пользователь заблокирован")

    # если баланс пользователя больше или равен сумме вывода и заяка ещё не принята
    if (ct.consumer.balance >= ct.value) and (ct.state != WithdrawTransaction.STATE_ACCEPTED):
        # вычетаем из баланса пользователя сумму
        ct.consumer.balance -= ct.value
        ct.consumer.frozenBalance -= ct.value
        # сохраняем пользователя
        ct.consumer.save()
        # меняем состояние заявки
        ct.state = WithdrawTransaction.STATE_ACCEPTED
        # сохраняем
        ct.save()

    return HttpResponseRedirect('/adminPanel/withdraw/list/0/')


# список читеров
def listCheater(request, cheated):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    # получаем queryset заявок с таким состоянием
    cs = ConsumerMarketCamp.objects.filter(stateCheated=int(cheated))

    # формируем удобный список для вывода на страницу
    cheaters = []
    for t in cs:
        cheaters.append({"tid": t.id, "link": t.link, "viewCnt": t.viewCnt,
                         "friendCnt": t.consumer.vkCnt})

    # делаем массив с заголовками для каждого из состояний
    return render(request,
                  'adminPanel/cheaters_list.html',
                  {"cheaters": cheaters,
                   "caption": ConsumerMarketCamp.cheatedStates[int(cheated)],
                   "state": int(cheated),
                   })


def cheaters(request):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    pretendCnt = ConsumerMarketCamp.objects.filter(stateCheated=ConsumerMarketCamp.STATE_PRETEND_CHEATED).count()

    return render(request,
                  'adminPanel/cheaters.html',
                  {"caption": "Панель администратора: читеры",
                   "pretendCnt": pretendCnt})


def punishCheater(request, c_id):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)
    cm = ConsumerMarketCamp.objects.get(pk=c_id)
    cm.stateCheated = ConsumerMarketCamp.STATE_CHEATED
    cm.save()
    if not cm.consumer.blocked:
        cm.consumer.blocked = True
        cm.consumer.save()

    return HttpResponseRedirect('/adminPanel/cheaters/list/1/')


def freeCheater(request, c_id):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)
    cm = ConsumerMarketCamp.objects.get(pk=c_id)
    cm.stateCheated = ConsumerMarketCamp.STATE_NOT_CHEATED
    cm.save()
    cm.consumer.blocked = False
    cm.consumer.save()

    return HttpResponseRedirect('/adminPanel/cheaters/list/1/')


# список читеров
def listBlocked(request):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    # делаем массив с заголовками для каждого из состояний
    return render(request,
                  'adminPanel/blocked_list.html',
                  {"cs": Consumer.objects.filter(blocked=True),
                   "caption": "Заблокированные"})


def freeBlocked(request, c_id):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)
    try:
        c = Consumer.objects.get(pk=c_id)
        c.blocked = False
        c.save()
    except:
        return getErrorPage(request, 'Ошибка поиска', 'Исполнитель не найден')

    return HttpResponseRedirect('/adminPanel/blocked/list/')
