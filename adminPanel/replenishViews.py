from django.http import HttpResponseRedirect
from django.shortcuts import render
from customer.models import ReplenishTransaction
from mainApp.code import is_member


def replenish(request):
    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/')

    template = 'adminPanel/replenish.html'
    context = {
    }
    return render(request, template, context)


def replenishNotAccepted(request):
    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/')

    ts = ReplenishTransaction.objects.filter(state=1).order_by('dt')

    transactions = []
    for t in ts:
        transactions.append({"date": t.dt.strftime("%d.%m.%y"), "value": t.value, "qiwi": t.customer.qiwi,
                             "tid": t.id})

    template = 'adminPanel/replenish_list.html'
    context = {
        "transactions": transactions,
        "caption": "Не обработанные заявки"
    }
    return render(request, template, context)


def replanishAccepted(request):
    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/')

    ts = ReplenishTransaction.objects.filter(state=3).order_by('dt')

    transactions = []
    for t in ts:
        transactions.append({"date": t.dt.strftime("%d.%m.%y"), "value": t.value, "qiwi": t.customer.qiwi,
                             "tid": t.id})

    template = 'adminPanel/replenish_list.html'
    context = {
        "transactions": transactions,
        "caption": "Принятые заявки"
    }
    return render(request, template, context)


def replenishRejected(request):
    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/')

    ts = ReplenishTransaction.objects.filter(state=2).order_by('dt')

    transactions = []
    for t in ts:
        transactions.append({"date": t.dt.strftime("%d.%m.%y"), "value": t.value, "qiwi": t.customer.qiwi,
                             "tid": t.id})

    template = 'adminPanel/replenish_list.html'
    context = {
        "transactions": transactions,
        "caption": "Отклонённые заявки"
    }
    return render(request, template, context)


def replenishReject(request, tid):
    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/')

    ts = ReplenishTransaction.objects.get(id=tid)
    ts.state = 2
    ts.save()

    return HttpResponseRedirect('/adminPanel/replenish/not-accepted/')


def replenishAccept(request, tid):
    if not is_member(request.user, "admins"):
        return HttpResponseRedirect('/replenish/')

    ts = ReplenishTransaction.objects.get(id=tid)
    c = ts.customer
    c.balance += ts.value
    c.save()
    ts.state = 3
    ts.save()

    return HttpResponseRedirect('/adminPanel/replenish/not-accepted/')
