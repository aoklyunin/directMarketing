# стартовая страница
from django.contrib import messages
from django.shortcuts import render

from mainApp.models import InfoText


def index(request):
    template = 'mainApp/index.html'
    it = InfoText.objects.get(pageName="index")
    context = {
        "user": request.user,
        "it": it,
        "caption": "DRPR"
    }
    return render(request, template, context)


def about(request):
    template = 'mainApp/about.html'
    it = InfoText.objects.get(pageName="about")
    context = {
        "user": request.user,
        "it": it,
        "caption": "О нас",
    }
    return render(request, template, context)


def customer(request):
    template = 'progressus/customer.html'
    it = InfoText.objects.get(pageName="customer")
    context = {
        "user": request.user,
        "it": it,
        "caption": "Заказчику",
    }
    return render(request, template, context)


def consumer(request):
    template = 'mainApp/consumer.html'
    it = InfoText.objects.get(pageName="consumer")
    context = {
        "user": request.user,
        "it": it,
        "caption": "Исполнителю",
    }
    return render(request, template, context)


def contact(request):
    template = 'mainApp/contact.html'
    it = InfoText.objects.get(pageName="contact")
    context = {
        "user": request.user,
        "it": it,
        "caption": "Обратная связь",
    }
    return render(request, template, context)


def customerTerms(request):
    template = 'mainApp/customer_terms.html'
    context = {
        "user": request.user,
        "caption" : "Заказчику",
    }
    return render(request, template, context)


def consumerTerms(request):
    template = 'mainApp/consumer_terms.html'
    context = {
        "user": request.user,
        "caption": "Исполнителю",
    }
    return render(request, template, context)
