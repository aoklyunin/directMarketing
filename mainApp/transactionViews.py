# -*- coding: utf-8 -*-
import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from mainApp.forms import ConsumerForm, CustomerForm, PaymentForm
from mainApp.models import Consumer, Customer, CustomerTransaction, ConsumerTransaction


def replenish(request):
    try:
        u = Customer.objects.get(user = request.user)
    except:
        HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = PaymentForm(request.POST)
        if form.is_valid():
            t = CustomerTransaction.objects.create(customer=u,value=form.cleaned_data["value"])
            return HttpResponseRedirect('/transactions/customer_detail/'+str(t.pk)+"/")

    template = 'transactions/replenish.html'
    qiwi = "+7 921 583 28 98"
    context = {
        "user": request.user,
        "form": PaymentForm(),
        "qiwi": qiwi,
    }
    return render(request, template, context)


def customer_detail(request, tid):
    template = 'transactions/customer_detail.html'
    context = {
        "user": request.user,
    }
    return render(request, template, context)


def withdraw(request):
    template = 'progressus/withdraw     .html'
    context = {
        "user": request.user,
    }
    return render(request, template, context)
