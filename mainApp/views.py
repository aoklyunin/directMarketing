# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse

from mainApp.code import is_member
from mainApp.forms import CommentForm
from mainApp.models import Comment, TehSupport


def test(request):
    return render_to_response('mainApp/test.html')


def getErrorPage(request, caption, msg):
    return render(request, "progressus/errorPage.html", {'caption': caption, "msg": msg})


def autorizedOnlyError(request):
    return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только авторизованным пользоавтелям')


# обработка комментария t - это куда надо добавить коммент
def processComment(request, t):
    try:
        cf = CommentForm(request.POST)
        if cf.is_valid():
            c = Comment.objects.create(dt=cf.cleaned_data["dt"], author=request.user,
                                       text=cf.cleaned_data["value"])
            t.comments.add(c)
        return HttpResponse("ye")
    except:
        return HttpResponse("no")


def tehSupport(request):
    # если пользователь не админ,
    if not request.user.is_authenticated():
        # переадресация на страницу с ошибкой
        return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только зарегестрированным пользователям')

    ClosedCnt = 0
    if is_member(request.user, "admins"):
        OpenedCnt = TehSupport.objects.filter(state=TehSupport.STATE_OPENED).count()
    else:
        OpenedCnt = 0

    if is_member(request.user, "admins"):
        # Получаем кол-во непрочитанных сообщений
        for rt in TehSupport.objects.all():
            cnt = rt.comments.filter(author=rt.author, readed=False).count()
            if rt.state == TehSupport.STATE_OPENED:
                OpenedCnt += cnt
            if rt.state == TehSupport.STATE_CLOSED:
                ClosedCnt += cnt
    else:
        # Получаем кол-во непрочитанных сообщений
        for rt in TehSupport.objects.filter(author=request.user):
            cnt = rt.comments.exclude(author=rt.author).filter(readed=False).count()
            if rt.state == TehSupport.STATE_OPENED:
                OpenedCnt += cnt
            if rt.state == TehSupport.STATE_CLOSED:
                ClosedCnt += cnt

    return render(request,
                  'mainApp/tehSupport.html',
                  {"caption": "Панель администратора: внесение",
                   "OpenedCnt": OpenedCnt, "ClosedCnt": ClosedCnt})


def createTehSupport(request):
    # если пользователь не админ,
    if not request.user.is_authenticated():
        # переадресация на страницу с ошибкой
        return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только зарегестрированным пользователям')
    if is_member(request.user, "admins"):
        return getErrorPage(request, 'Ошибка доступа', 'Админ не может подать заявку в тех. поддержку')

    t = TehSupport.objects.create(author=request.user)
    t.save()
    return HttpResponseRedirect('/tehsupport/detail/' + str(t.pk) + '/')


def tehSupportList(request, state):
    # если пользователь не админ,
    if not request.user.is_authenticated():
        # переадресация на страницу с ошибкой
        return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только зарегестрированным пользователям')

        # формируем удобный список для вывода на страницу
    transactions = []
    if is_member(request.user, "admins"):
        for t in TehSupport.objects.filter(state=state):
            transactions.append({"date": t.dt.strftime("%d.%m.%y"), "pk": t.pk,
                                 "notReadedCnt": t.comments.filter(author=t.author, readed=False).count()})
    else:
        for t in TehSupport.objects.filter(state=state, author=request.user):
            transactions.append({"date": t.dt.strftime("%d.%m.%y"), "pk": t.pk,
                                 "notReadedCnt": t.comments.exclude(author=t.author).filter(readed=False).count()})
    # делаем массив с заголовками для каждого из состояний
    return render(request,
                  'mainApp/tehSupport_list.html',
                  {"transactions": transactions,
                   "caption": "Заявки в тех. поддержку: " + TehSupport.states[int(state)], "state": state})


def detailTehSupport(request, tid):
    t = TehSupport.objects.get(id=tid)
    if not request.user.is_authenticated():
        # переадресация на страницу с ошибкой
        return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только зарегестрированным пользователям')

    # обработка комментария
    if request.method == 'POST':
        try:
            cf = CommentForm(request.POST)
            #  print(cf)
            if cf.is_valid():
                c = Comment.objects.create(dt=cf.cleaned_data["dt"], author=request.user,
                                           text=cf.cleaned_data["value"])
                t.comments.add(c)
                if t.state == TehSupport.STATE_CLOSED:
                    t.state = TehSupport.STATE_OPENED
                    t.save()
        except:
            print("Ошибка обработки комментария")

    if request.user == t.author:
        t.comments.exclude(author=t.author).filter(readed=False).update(readed=True)
    else:
        t.comments.filter(author=t.author, readed=False).update(readed=True)

    # получаем последние 6 комментариев
    comments = []
    for c in t.comments.order_by('dt'):
        comments.append({"text": c.text.replace("\n", " "), "isUsers": "false" if c.author == request.user else "true",
                         "name": c.author.first_name, "date": c.dt.strftime("%H:%M")})

    # получаем картинки для чата
    if request.user == t.author:
        from_av = "images/customer_avatar.jpg"
        to_av = "images/admin_avatar.jpg"
    else:
        from_av = "images/admin_avatar.jpg"
        to_av = "images/customer_avatar.jpg"

    context = {
        "caption": "Заяка №" + str(t.pk),
        "comments": comments,
        "target": "/tehsupport/detail/" + tid + "/",
        "from_av": from_av,
        "to_av": to_av,
        "tid": tid,
        "isAdmin": is_member(request.user, "admins")
    }
    return render(request, 'mainApp/tehSupport_detail.html', context)


def closeTehSupport(request, tid):
    # если пользователь не админ,
    if not is_member(request.user, "admins"):
        # переадресация на страницу с ошибкой
        return getErrorPage(request, 'Ошибка доступа', 'Эта страница доступна только администраторам')

    t = TehSupport.objects.get(id=tid)
    t.state = TehSupport.STATE_CLOSED
    t.save()

    return HttpResponseRedirect('/tehsupport/')
