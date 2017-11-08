# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from consumer.models import Consumer
from customer.models import Customer
from mainApp.code import is_member
from mainApp.forms import RegisterCustomerForm, RegisterConsumerForm, LoginForm
from mainApp.models import InfoText


def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            # пробуем залогиниться
            user = auth.authenticate(username=login, password=password)
            # если полльзователь существует и он активен
            if user is not None and user.is_active:
                # входим на сайт
                auth.login(request, user)
                if is_member(user, "admins"):
                    return HttpResponseRedirect("/adminPanel/")
                if is_member(user, "consumers"):
                    return HttpResponseRedirect("/consumer/")
                if is_member(user, "customers"):
                    return HttpResponseRedirect("/customer/")
                return HttpResponseRedirect('/')
            else:
                messages.error(request, "пара логин-пароль не найдена")
    form = LoginForm()

    template = 'mainApp/signin.html'
    context = {
        "user": request.user,
        "form": form,
        "caption": "Вход"
    }
    return render(request, template, context)


def signup(request):
    template = 'mainApp/signup.html'
    it = InfoText.objects.get(pageName="signup")
    context = {
        "user": request.user,
        "it": it,
        "caption": "Регистрация"
    }
    return render(request, template, context)


def signup_customer(request):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            # проверяем, что пароли совпадают
            if form.cleaned_data["password"] != form.cleaned_data["rep_password"]:
                # выводим сообщение и перезаполняем форму
                messages.error(request, "пароли не совпадают")
                form = RegisterCustomerForm(initial={'mail': form.cleaned_data["mail"],
                                                     'name': form.cleaned_data["name"],
                                                     'second_name': form.cleaned_data["second_name"],
                                                     'acceptedTerms': True})
            else:
                # получаем данные из формы
                mail = form.cleaned_data["mail"]
                name = form.cleaned_data["name"]
                second_name = form.cleaned_data["second_name"]
                password = form.cleaned_data["password"]
                try:
                    # создаём пользователя
                    user = User.objects.create_user(username=mail,
                                                    email=mail,
                                                    password=password)
                    # если получилось создать пользователя
                    if user:
                        # задаём ему имя и фамилию
                        user.first_name = name
                        user.last_name = second_name
                        # созраняем пользователя
                        user.save()
                        auth.login(request, user)
                        # создаём студента
                        c = Customer.objects.create(user=user)
                        # сохраняем студента
                        c.save()
                        return HttpResponseRedirect("/customer/")
                    else:
                        messages.error("Ошибка создания пользователя")
                except:
                    # если не получилось создать пользователя, то выводим сообщение
                    messages.error(request, "Такой пользователь уже существует")
                    form = RegisterCustomerForm(initial={'mail': form.cleaned_data["mail"],
                                                         'name': form.cleaned_data["name"],
                                                         'second_name': form.cleaned_data["second_name"],
                                                         'acceptedTerms': True})
    else:
        form = RegisterCustomerForm()

    template = 'mainApp/signup_customer.html'
    # print(form)
    context = {
        "user": request.user,
        "form": form,
        "caption": "Регистрация заказчика"
    }
    return render(request, template, context)


def signup_consumer(request):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = RegisterConsumerForm(request.POST)
        if form.is_valid():
            # проверяем, что пароли совпадают
            if form.cleaned_data["password"] != form.cleaned_data["rep_password"]:
                # выводим сообщение и перезаполняем форму
                messages.error(request, "пароли не совпадают")
                form = RegisterConsumerForm(initial={'mail': form.cleaned_data["mail"],
                                                     'acceptedTerms': True})
            else:
                # получаем данные из формы
                mail = form.cleaned_data["mail"]
                password = form.cleaned_data["password"]
                try:
                    # создаём пользователя
                    user = User.objects.create_user(username=mail,
                                                    email=mail,
                                                    password=password)
                    # если получилось создать пользователя
                    if user:
                        auth.login(request, user)
                        # создаём студента
                        c = Consumer.objects.create(user=user)
                        # сохраняем студента
                        c.save()
                        return HttpResponseRedirect("/consumer/")
                    else:
                        messages.error("Ошибка создания пользователя")

                except:
                    # если не получилось создать пользователя, то выводим сообщение
                    messages.error(request, "Такой пользователь уже существует")
                    form = RegisterConsumerForm(initial={'mail': form.cleaned_data["mail"],
                                                         'acceptedTerms': True})
    else:
        form = RegisterConsumerForm()

    template = 'mainApp/signup_consumer.html'
    context = {
        "user": request.user,
        "form": form,
        "caption": "Регистрация исполнителя"

    }
    return render(request, template, context)


def signout(request):
    logout(request)
    return HttpResponseRedirect("/")
