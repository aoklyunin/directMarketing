# -*- coding: utf-8 -*-
import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from mainApp.forms import ConsumerForm, CustomerForm, PaymentForm, TextForm
from mainApp.models import Consumer, Customer, CustomerTransaction, ConsumerTransaction, Comment


def replenish(request):
    try:
        u = Customer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = PaymentForm(request.POST)
        if form.is_valid():
            t = CustomerTransaction.objects.create(customer=u, value=form.cleaned_data["value"])
            return HttpResponseRedirect('/transactions/customer_detail/' + str(t.pk) + "/")

    template = 'transactions/replenish.html'
    qiwi = "+7 921 583 28 98"
    context = {
        "user": request.user,
        "form": PaymentForm(),
        "qiwi": qiwi,
    }
    return render(request, template, context)


def customer_detail(request, tid):
    ct = CustomerTransaction.objects.get(id=tid)
    if not (request.user.is_staff or request.user == ct.customer.user):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = TextForm(request.POST)
        if form.is_valid():
            c = Comment.objects.create(author=request.user, text=form.cleaned_data["value"])
            ct.comments.add(c)

    template = 'transactions/customer_detail.html'
    context = {
        "id": tid,
        "need_pay": ct.state == 0,
        "date": ct.dt.strftime("%d.%m.%y"),
        "state": CustomerTransaction.states[ct.state],
        "user": request.user,
        "comments": ct.comments.order_by('dt'),
        "form": TextForm(),
    }
    return render(request, template, context)


def customer_transaction_set_user_payed(request, tid):
    ct = CustomerTransaction.objects.get(id=tid)
    if ct.customer.user == request.user:
        ct.state = 1
        ct.save()
        return HttpResponseRedirect('/transactions/customer_detail/' + str(tid) + '/')
    else:
        return HttpResponseRedirect('/')


def withdraw(request):
    template = 'progressus/withdraw.html'
    context = {
        "user": request.user,
    }
    return render(request, template, context)


def replanishAdmin(request):
    if not request.user.is_staff:
        HttpResponseRedirect('/')

    template = 'transactions/admin_replenish.html'
    context = {
        "user": request.user,

    }
    return render(request, template, context)


def withdrawAdmin(request):
    return None


def replanishAdminNotComplete(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/')

    ts = CustomerTransaction.objects.filter(state=1).order_by('dt')

    transactions = []
    for t in ts:
        transactions.append({"date": t.dt.strftime("%d.%m.%y"), "value": t.value, "qiwi": t.customer.qiwi,
                             "tid": t.id})

    template = 'transactions/admin_replenish_list.html'
    context = {
        "user": request.user,
        "transactions": transactions,
        "caption": "Не завершённые заявки"
    }
    return render(request, template, context)


def replanishAdminComplete(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/')

    ts = CustomerTransaction.objects.filter(state=3).order_by('dt')

    transactions = []
    for t in ts:
        transactions.append({"date": t.dt.strftime("%d.%m.%y"), "value": t.value, "qiwi": t.customer.qiwi,
                             "tid": t.id})

    template = 'transactions/admin_replenish_list.html'
    context = {
        "user": request.user,
        "transactions": transactions,
        "caption": "Принятые заявки"
    }
    return render(request, template, context)


def replanishAdminRejected(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/')

    ts = CustomerTransaction.objects.filter(state=2).order_by('dt')

    transactions = []
    for t in ts:
        transactions.append({"date": t.dt.strftime("%d.%m.%y"), "value": t.value, "qiwi": t.customer.qiwi,
                             "tid": t.id})

    template = 'transactions/admin_replenish_list.html'
    context = {
        "user": request.user,
        "transactions": transactions,
        "caption": "Отклонённые заявки"
    }
    return render(request, template, context)


def replanishAdminReject(request, tid):
    if not request.user.is_staff:
        return HttpResponseRedirect('/')

    ts = CustomerTransaction.objects.get(id=tid)
    ts.state = 2
    ts.save()

    return HttpResponseRedirect('/replenish/admin/not-complete/')


def replanishAdminAccept(request, tid):
    if not request.user.is_staff:
        return HttpResponseRedirect('/')

    ts = CustomerTransaction.objects.get(id=tid)
    c = ts.customer
    c.balance += ts.value
    c.save()
    ts.state = 3
    ts.save()

    return HttpResponseRedirect('/replenish/admin/not-complete/')
