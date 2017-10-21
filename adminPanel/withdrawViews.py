from django.http import HttpResponseRedirect
from django.shortcuts import render

from consumer.models import WithdrawTransaction
from mainApp.code import is_member


def withdraw(request):
    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/')

    template = 'adminPanel/withdraw.html'
    context = {
    }
    return render(request, template, context)


def withdrawNotAccepted(request):
    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/')

    ts = WithdrawTransaction.objects.filter(state=0).order_by('dt')

    transactions = []
    for t in ts:
        transactions.append({"date": t.dt.strftime("%d.%m.%y"), "value": t.value, "qiwi": t.consumer.qiwi,
                             "tid": t.id, "canNotPay": t.value > t.consumer.balance, "balance": t.consumer.balance})

    template = 'adminPanel/withdraw_list.html'
    context = {
        "transactions": transactions,
        "caption": "Не обработанные заявки"
    }
    return render(request, template, context)


def withdrawAccepted(request):
    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/')

    ts = WithdrawTransaction.objects.filter(state=1).order_by('dt')

    transactions = []
    for t in ts:
        transactions.append({"date": t.dt.strftime("%d.%m.%y"), "value": t.value, "qiwi": t.customer.qiwi,
                             "tid": t.id})

    template = 'adminPanel/withdraw_list.html'
    context = {
        "transactions": transactions,
        "caption": "Принятые заявки"
    }
    return render(request, template, context)


def withdrawRejected(request):
    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/')

    ts = WithdrawTransaction.objects.filter(state=2).order_by('dt')

    transactions = []
    for t in ts:
        transactions.append({"date": t.dt.strftime("%d.%m.%y"), "value": t.value, "qiwi": t.customer.qiwi,
                             "tid": t.id})

    template = 'adminPanel/withdraw_list.html'
    context = {
        "transactions": transactions,
        "caption": "Отклонённые заявки"
    }
    return render(request, template, context)


def withdrawReject(request, tid):
    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/')

    ts = WithdrawTransaction.objects.get(id=tid)
    ts.state = 2
    ts.save()

    return HttpResponseRedirect('/adminPanel/withdraw/not-accepted/')


def withdrawAccept(request, tid):
    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/')

    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/')

    ct = WithdrawTransaction.objects.get(id=tid)
    if (ct.consumer.balance > ct.value):
        ct.consumer.balance -= ct.value
        ct.consumer.save()
        ct.state = 1
        ct.save()

    return HttpResponseRedirect('/adminPanel/withdraw/not-accepted/')
