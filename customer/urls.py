from django.conf.urls import url

from customer.views import balance, campanies, index, replenish, replenish_detail, terms, replenish_set_payed, \
    detailCampany, createCampany, stopCampany, startCampany, campamy_discuss, modifyCampany

urlpatterns = [

    url(r'^balance/$', balance),
    url(r'^campanies/$', campanies),
    url(r'^campany/detail/(?P<tid>[0-9]+)/$', detailCampany),
    url(r'^campany/modify/(?P<tid>[0-9]+)/$', modifyCampany),
    url(r'^campany/discuss/(?P<tid>[0-9]+)/$', campamy_discuss),
    url(r'^campany/create/$', createCampany),
    url(r'^campany/start/(?P<tid>[0-9]+)/$', startCampany),
    url(r'^campany/stop/(?P<tid>[0-9]+)/$', stopCampany),
    url(r'^replenish/detail/(?P<tid>[0-9]+)/$', replenish_detail),
    url(r'^replenish/set_payed/(?P<tid>[0-9]+)/$', replenish_set_payed),
    url(r'^replenish/$', replenish),
    url(r'^terms/$', terms),
    url(r'^', index)
]
