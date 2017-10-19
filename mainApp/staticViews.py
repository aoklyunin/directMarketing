# стартовая страница
from django.contrib import messages
from django.shortcuts import render

from mainApp.models import InfoText


def index(request):
    template = 'progressus/index.html'
    it = InfoText.objects.get(pageName="index")
    context = {
        "user": request.user,
        "it": it
    }
    return render(request, template, context)


def about(request):
    template = 'progressus/about.html'
    it = InfoText.objects.get(pageName="about")
    context = {
        "user": request.user,
        "it": it
    }
    return render(request, template, context)


def customer(request):
    template = 'progressus/customer.html'
    it = InfoText.objects.get(pageName="customer")
    context = {
        "user": request.user,
        "it": it
    }
    return render(request, template, context)


def consumer(request):
    template = 'progressus/consumer.html'
    it = InfoText.objects.get(pageName="consumer")
    context = {
        "user": request.user,
        "it": it
    }
    return render(request, template, context)


def contact(request):
    template = 'progressus/contact.html'
    it = InfoText.objects.get(pageName="contact")
    context = {
        "user": request.user,
        "it": it
    }
    return render(request, template, context)



def consumer_terms(request):
    template = 'progressus/consumer_terms.html'
    context = {
        "user": request.user,
    }
    return render(request, template, context)
