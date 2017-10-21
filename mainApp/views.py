# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response

def test(request):
    return render_to_response('mainApp/test.html')