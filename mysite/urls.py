# -*- coding: utf-8 -*-
# обработчик адресов сайта
from django.conf.urls import include, url
from django.contrib import admin
import mainApp.staticViews
import mainApp.auth
import mainApp.views

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
    url(r'^signout/$', mainApp.auth.signout),
    url(r'^signup/consumer/$', mainApp.auth.signup_consumer),
    url(r'^signup/customer/$', mainApp.auth.signup_customer),
    url(r'^customer_terms/$', mainApp.staticViews.customer_terms),
    url(r'^consumer_terms/$', mainApp.staticViews.consumer_terms),
    url(r'^personal/main/$', mainApp.views.personal_main),
    url(r'^personal/balance/$', mainApp.views.personal_balance),
    url(r'^personal/marketing/$', mainApp.views.personal_marketing),
    url(r'^', mainApp.staticViews.index, name='index')
]
