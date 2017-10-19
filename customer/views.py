from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from customer.models import Customer, ReplenishTransaction
from mainApp.code import is_member
from mainApp.forms import CustomerForm, PaymentForm, TextForm
from mainApp.models import Comment


def index(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect('/')

    try:
        us = Customer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = CustomerForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            us.qiwi = form.cleaned_data['qiwi']
            us.companyName = form.cleaned_data['name']
            us.save()

    form = CustomerForm(initial={'name': us.companyName, 'qiwi': us.qiwi})
    template = 'customer/index.html'

    context = {
        "u": us,
        "form": form,
    }
    return render(request, template, context)


def balance(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect('/')

    try:
        u = Customer.objects.get(user=request.user)
    except:
        HttpResponseRedirect('/')

    ts = ReplenishTransaction.objects.filter(customer=u).order_by('dt')
    transactions = []
    for t in ts:
        transactions.append({"date": t.dt, "value": t.value, "state": ReplenishTransaction.states[t.state],
                             "tid": t.id})
    template = 'customer/balance.html'
    context = {
        "u": u,
        "transactions": transactions,
    }
    return render(request, template, context)


def campanies(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect('/')

    try:
        us = Customer.objects.get(user=request.user)
    except:
        HttpResponseRedirect('/')

    template = 'customer/campanies.html'
    context = {
    }
    return render(request, template, context)


def replenish(request):
    try:
        u = Customer.objects.get(user=request.user)
    except:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = PaymentForm(request.POST)
        if form.is_valid():
            t = ReplenishTransaction.objects.create(customer=u, value=form.cleaned_data["value"])
            return HttpResponseRedirect('/customer/replenish_detail/' + str(t.pk) + "/")

    template = 'customer/replenish.html'
    qiwi = "+7 921 583 28 98"
    context = {
        "form": PaymentForm(),
        "qiwi": qiwi,
    }
    return render(request, template, context)


def replenish_detail(request, tid):
    ct = ReplenishTransaction.objects.get(id=tid)
    if not(is_member(request.user, "admins") or request.user == ct.customer.user):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        # строим форму на основе запроса
        form = TextForm(request.POST)
        if form.is_valid():
            c = Comment.objects.create(author=request.user, text=form.cleaned_data["value"])
            ct.comments.add(c)

    template = 'customer/replenish_detail.html'
    context = {
        "id": tid,
        "need_pay": ct.state == 0,
        "date": ct.dt.strftime("%d.%m.%y"),
        "state": ReplenishTransaction.states[ct.state],
        "comments": ct.comments.order_by('dt'),
        "form": TextForm(),
    }
    return render(request, template, context)


def terms(request):
    template = 'customer/terms.html'
    context = {
        "user": request.user,
    }
    return render(request, template, context)


def replenish_set_payed(request, tid):
    ct = ReplenishTransaction.objects.get(id=tid)
    if ct.customer.user == request.user:
        ct.state = 1
        ct.save()
        return HttpResponseRedirect('/customer/replenish_detail/' + str(tid) + "/")
    else:
        return HttpResponseRedirect('/')

