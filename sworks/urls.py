# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.attempt, name='index'),
    url(r'^attemptList$', views.attemptList, name='attemptList')

]
