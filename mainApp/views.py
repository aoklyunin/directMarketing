# -*- coding: utf-8 -*-
import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from mainApp.forms import ConsumerForm, CustomerForm
from mainApp.models import Consumer, Customer, CustomerTransaction, ConsumerTransaction


def personal_main(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect('/')

    flg = 0
    try:
        us = Consumer.objects.get(user=request.user)
        flg = 1
    except:
        try:
            us = Customer.objects.get(user=request.user)
            flg = 2
        except:
            HttpResponseRedirect('/')

    if flg == 1:
        if request.method == 'POST':
            # строим форму на основе запроса
            form = ConsumerForm(request.POST)
            if form.is_valid():
                us.qiwi = form.cleaned_data['qiwi']
                us.save()
                u = us.user
                u.first_name = form.cleaned_data['name']
                u.last_name = form.cleaned_data['second_name']
                u.save()

        form = ConsumerForm(initial={'qiwi': us.qiwi, 'name': us.user.first_name, 'second_name': us.user.last_name})
        template = 'consumer/main.html'
    else:
        if request.method == 'POST':
            # строим форму на основе запроса
            form = CustomerForm(request.POST)

            if form.is_valid():
                print(form.cleaned_data)
                us.qiwi = form.cleaned_data['qiwi']
                us.companyName = form.cleaned_data['name']
                us.save()

        form = CustomerForm(initial={'name': us.companyName, 'qiwi': us.qiwi})
        template = 'customer/main.html'

    context = {
        "user": request.user,
        "u": us,
        "flg": flg,
        "form": form,
    }
    return render(request, template, context)


def personal_balance(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect('/')

    flg = 0
    try:
        u = Consumer.objects.get(user=request.user)
        flg = 1
    except:
        try:
            u = Customer.objects.get(user=request.user)
            flg = 2
        except:
            HttpResponseRedirect('/')

    if flg == 1:
        ts = ConsumerTransaction.objects.filter(consumer=u).order_by('dt')
        transactions = []
        for t in ts:
            transactions.append({"date": t.dt, "value": t.value, "state": ConsumerTransaction.states[t.state],
                                 "tid": t.id})
        template = 'consumer/balance.html'
    else:
        ts = CustomerTransaction.objects.filter(customer=u).order_by('dt')
        transactions = []
        for t in ts:
            transactions.append({"date": t.dt, "value": t.value, "state": ConsumerTransaction.states[t.state],
                                 "tid": t.id})
        template = 'customer/balance.html'
    context = {
        "user": request.user,
        "u": u,
        "transactions": transactions,
    }
    return render(request, template, context)


def personal_marketing(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect('/')

    flg = 0
    try:
        Consumer.objects.get(user=request.user)
        flg = 1
    except:
        try:
            Customer.objects.get(user=request.user)
            flg = 2
        except:
            HttpResponseRedirect('/')

    if flg == 1:
        template = 'consumer/marketing.html'
    else:
        template = 'customer/marketing.html'
    context = {
        "user": request.user,
    }
    return render(request, template, context)
