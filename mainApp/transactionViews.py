# -*- coding: utf-8 -*-
import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from customer.models import Customer, ReplenishTransaction
from mainApp.forms import ConsumerForm, CustomerForm, PaymentForm, TextForm
from mainApp.models import  Comment


def withdraw(request):
    template = 'progressus/withdraw.html'
    context = {
        "user": request.user,
    }
    return render(request, template, context)



