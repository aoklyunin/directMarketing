# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse

from mainApp.forms import CommentForm
from mainApp.models import Comment


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
