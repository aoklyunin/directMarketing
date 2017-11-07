from django.http import HttpResponseRedirect
from django.shortcuts import render
from consumer.models import WithdrawTransaction
from customer.models import MarketCamp, ReplenishTransaction
from mainApp.code import is_member

# получить страницу ошибки доступа к админской странице
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

    return render(request,
                  'adminPanel/replenish.html',
                  {"caption": "Панель администратора: внесение"})


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
                             "tid": t.id})

    return render(request,
                  'adminPanel/replenish_list.html',
                  {"transactions": transactions, "caption": ReplenishTransaction.list_states[st], "state": st})


# Отклонить завку
def replenishReject(request, tid):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    ts = ReplenishTransaction.objects.get(id=tid)
    ts.state = ReplenishTransaction.STATE_REJECTED
    ts.save()

    return HttpResponseRedirect('/adminPanel/replenish/list/1/')


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

    return render(request,
                  'adminPanel/withdraw.html',
                  {"caption": "Панель администратора: вывод"})


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
        transactions.append({"date": t.dt.strftime("%d.%m.%y"), "value": t.value, "qiwi": t.consumer.qiwi,
                             "tid": t.id, "canNotPay": t.value > t.consumer.balance, "balance": t.consumer.balance})

    # делаем массив с заголовками для каждого из состояний
    return render(request,
                  'adminPanel/withdraw_list.html',
                  {"transactions": transactions,
                   "caption": WithdrawTransaction.list_states[st], "state": st})


# Отклонить завку
def withdrawReject(request, tid):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    ts = WithdrawTransaction.objects.get(id=tid)
    ts.state = WithdrawTransaction.STATE_REJECTED
    ts.save()

    return HttpResponseRedirect('/adminPanel/withdraw/list/0/')


# Принять завку
def withdrawAccept(request, tid):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    ct = WithdrawTransaction.objects.get(id=tid)
    # если баланс пользователя больше или равен сумме вывода и заяка ещё не принята
    if (ct.consumer.balance >= ct.value) and (ct.state != WithdrawTransaction.STATE_ACCEPTED):
        # вычетаем из баланса пользователя сумму
        ct.consumer.balance -= ct.value
        # сохраняем пользователя
        ct.consumer.save()
        # меняем состояние заявки
        ct.state = WithdrawTransaction.STATE_ACCEPTED
        # сохраняем
        ct.save()

    return HttpResponseRedirect('/adminPanel/withdraw/list/0/')


# проверка на бота
def checkBot(request):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)
