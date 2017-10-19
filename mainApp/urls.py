# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
import mainApp.staticViews
import mainApp.auth
import mainApp.views
import mainApp.transactionViews

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# автоопределение администратора
from mysite import settings

urlpatterns = [
    # url(r'^$', views.attempt, name='index'),
    # url(r'^attemptList$', views.attemptList, name='attemptList')
]
