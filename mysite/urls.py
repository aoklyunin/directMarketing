# -*- coding: utf-8 -*-
# обработчик адресов сайта
from django.conf.urls import include, url
from django.contrib import admin
import sworks.auth
import sworks.views

# автоопределение администратора
admin.autodiscover()

urlpatterns = [
    # добавить задание
    url(r'^addTask/$', sworks.views.addTask),
    # панель администратора
    url(r'^admin/', include(admin.site.urls)),
    # выход из сайта
    url(r'^logout/$', sworks.auth.logout_view),
    # регистрация на сайте
    url(r'^register/$', sworks.auth.register),
    # просмотр задания
    url(r'^mark/detail/(?P<mark_id>[0-9]+)/$', sworks.views.mark_detail),
    # попросить оценки
    url(r'^mark/needCheck/(?P<mark_id>[0-9]+)/$', sworks.views.markMakeNeedCheck),
    url(r'^mark/list/$', sworks.views.markNeedCheckList),
    url(r'^mark/list_accepted/$', sworks.views.mark_list_accepted),
    url(r'^mark/list_not_accepted/$', sworks.views.mark_list_not_accepted),
    url(r'^mark/list_marked/$', sworks.views.mark_list_marked),
    # принять попытку
    url(r'^mark/mark/(?P<mark_id>[0-9]+)/(?P<state_val>[0-9]+)/$', sworks.views.doMark),
    # личный кабинет
    url(r'^personal/$', sworks.views.personal),
    # стартовая страница
    url(r'^', sworks.auth.index, name='index'),

]
