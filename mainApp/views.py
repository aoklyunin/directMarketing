# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse


def test(request):
    return render_to_response('mainApp/test.html')


def getErrorPage(request, caption, msg):
    return render(request, "progressus/errorPage.html", {'caption': caption, "msg": msg})
