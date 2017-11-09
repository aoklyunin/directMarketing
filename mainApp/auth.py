# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from consumer.models import Consumer
from customer.models import Customer
from mainApp.code import is_member
from mainApp.forms import RegisterCustomerForm, RegisterConsumerForm, LoginForm
from mainApp.localCode import account_activation_token
from mainApp.models import InfoText
from mainApp.views import getErrorPage


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
                messages.error(request, "пара логин-пароль не найдена или пользователь не подтверждён")

    form = LoginForm()

    template = 'registration/signin.html'
    context = {
        "user": request.user,
        "form": form,
        "caption": "Вход"
    }
    return render(request, template, context)


def signup(request):
    template = 'registration/signup.html'
    it = InfoText.objects.get(pageName="signup")
    context = {
        "user": request.user,
        "it": it,
        "caption": "Регистрация"
    }
    return render(request, template, context)


def writeMsgConfim(request, to_email, user):
    current_site = get_current_site(request)
    message = render_to_string('registration/mailVerification.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    mail_subject = 'Активируйте Вашу учётную запись.'
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


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
                        user.is_active = False
                        # созраняем пользователя
                        user.save()
                        g = Group.objects.get(name='customers')
                        g.user_set.add(user)

                        # auth.login(request, user)
                        # создаём студента
                        c = Customer.objects.create(user=user)
                        # сохраняем студента
                        c.save()
                        writeMsgConfim(request, mail, user)
                        return mailConfirmPage(request, user)
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

    template = 'registration/signup_customer.html'
    # print(form)
    context = {
        "user": request.user,
        "form": form,
        "caption": "Регистрация заказчика"
    }
    return render(request, template, context)


def mailConfirmPage(request, user):
    template = 'progressus/simpleMinPanelPage.html'
    context = {
        "user": user,
        "text": "Для входа Вам необходимо подтвердить свою электронную почту. Письмо с инструкцией будет выслано Вам в ближайшее время.",
        "caption": "Подтвердите свою почту",
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
                name = form.cleaned_data["name"]
                try:
                    # создаём пользователя
                    user = User.objects.create_user(username=mail,
                                                    email=mail,
                                                    password=password)
                    # если получилось создать пользователя
                    if user:
                        # auth.login(request, user)
                        user.is_active = False
                        user.first_name = name
                        user.save()
                        g = Group.objects.get(name='consumers')
                        g.user_set.add(user)

                        # создаём студента
                        c = Consumer.objects.create(user=user)
                        # сохраняем студента
                        c.save()
                        writeMsgConfim(request, mail, user)
                        return mailConfirmPage(request, user)
                    else:
                        messages.error("Ошибка создания пользователя")

                except:
                    # если не получилось создать пользователя, то выводим сообщение
                    messages.error(request, "Такой пользователь уже существует")
                    form = RegisterConsumerForm(initial={'mail': form.cleaned_data["mail"],
                                                         'acceptedTerms': True})
    else:
        form = RegisterConsumerForm()

    template = 'registration/signup_consumer.html'
    context = {
        "user": request.user,
        "form": form,
        "caption": "Регистрация исполнителя"

    }
    return render(request, template, context)


def signout(request):
    logout(request)
    return HttpResponseRedirect("/")
