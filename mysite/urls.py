# -*- coding: utf-8 -*-
# обработчик адресов сайта
from django.conf.urls import include, url
from django.contrib import admin
import mainApp.staticViews
import mainApp.auth

# автоопределение администратора
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', mainApp.staticViews.about),
    url(r'^customer/$', mainApp.staticViews.customer),
    url(r'^consumer/$', mainApp.staticViews.consumer),
    url(r'^contact/$', mainApp.staticViews.contact),
    url(r'^signin/$', mainApp.auth.signin),
    url(r'^signup/$', mainApp.auth.signup),
    url(r'^', mainApp.staticViews.index, name='index')
]
