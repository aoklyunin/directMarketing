from django.conf.urls import url

from consumer.views import balance, campanies, index, terms, detailCampany, withdrawDetail, \
    withdraw, autoWithdraw, getCode, processCode, postVKview, campaniesMain, process

urlpatterns = [

    url(r'^balance/$', balance),
    url(r'^withdraw/detail/(?P<tid>[0-9]+)/$', withdrawDetail),
    url(r'^withdraw/$', withdraw),
    url(r'^withdraw/auto/(?P<tp>[0-9])/$', autoWithdraw),
    url(r'^terms/$', terms),
    url(r'^vk/getCode/$', getCode),
    url(r'^vk/processCode/$', processCode),
    url(r'^vk/post/$', postVKview),
    url(r'^campanies/$', campaniesMain),
    url(r'^campanies/(?P<tp>[0-9])/$', campanies),
    url(r'^campany/detail/(?P<tid>[0-9]+)/$', detailCampany),
    url(r'^process/$', process),
    url(r'^', index)
]
