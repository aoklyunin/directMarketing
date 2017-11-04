# -*- coding: utf-8 -*-
# обработчик адресов сайта
from django.conf.urls import include, url
from django.contrib import admin
import mainApp.views
import mainApp.staticViews
import mainApp.auth

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', mainApp.staticViews.about),
    url(r'^contact/$', mainApp.staticViews.contact),
    url(r'^signin/$', mainApp.auth.signin),
    url(r'^signup/$', mainApp.auth.signup),
    url(r'^signout/$', mainApp.auth.signout),
    url(r'^signup/consumer/$', mainApp.auth.signup_consumer),
    url(r'^signup/customer/$', mainApp.auth.signup_customer),
    url(r'^test/$', mainApp.views.test),

    # Notice the expression does not end in $,
    # that happens at the myapp/url.py level
    url(r'^adminPanel/', include('adminPanel.urls')),
    url(r'^customer/', include('customer.urls')),
    url(r'^consumer/', include('consumer.urls')),
    url(r'^terms/customer/$', mainApp.staticViews.customerTerms),
    url(r'^terms/consumer/$', mainApp.staticViews.consumerTerms),
    url(r'^', mainApp.staticViews.index, name='index')

]
