from django.http import HttpResponseRedirect
from django.shortcuts import render
from adminPanel.views import adminError
from customer.models import ReplenishTransaction
from mainApp.code import is_member


# внесение средств
def replenish(request):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return adminError(request)

    return render(request,
                  'adminPanel/replenish.html',
                  {"caption": "Админ: пополнение баланса"})


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
