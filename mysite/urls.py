# -*- coding: utf-8 -*-
# обработчик адресов сайта
from django.conf.urls import include, url
from django.contrib import admin
import mainApp.auth
import mainApp.views

# автоопределение администратора
admin.autodiscover()

urlpatterns = [
    # добавить задание
   # url(r'^addTask/$', mainApp.views.addTask),
    # панель администратора
    url(r'^admin/', include(admin.site.urls)),
    # выход из сайта
   # url(r'^logout/$', mainApp.auth.logout_view),
    # регистрация на сайте
   # url(r'^register/$', mainApp.auth.register),
    # просмотр задания
 #   url(r'^mark/detail/(?P<mark_id>[0-9]+)/$', mainApp.views.mark_detail),
  #  # попросить оценки
   # url(r'^mark/needCheck/(?P<mark_id>[0-9]+)/$', mainApp.views.markMakeNeedCheck),
   # url(r'^mark/list/$', mainApp.views.markNeedCheckList),
  #  url(r'^mark/list_accepted/$', mainApp.views.mark_list_accepted),
  #  url(r'^mark/list_not_accepted/$', mainApp.views.mark_list_not_accepted),
  #  url(r'^mark/list_marked/$', mainApp.views.mark_list_marked),
  #  # принять попытку
  #  url(r'^mark/mark/(?P<mark_id>[0-9]+)/(?P<state_val>[0-9]+)/$', mainApp.views.doMark),
    # личный кабинет
   # url(r'^personal/$', mainApp.views.personal),
    # стартовая страница
    url(r'^', mainApp.auth.index, name='index'),

]
