from django.conf.urls import url

from customer.views import campanies, index, replenish, replenish_detail, replenish_set_payed, \
    detailCampany, createCampany, stopCampany, startCampany, modifyCampany

urlpatterns = [
    url(r'^campanies/$', campanies),
    url(r'^campany/detail/(?P<tid>[0-9]+)/$', detailCampany),
    url(r'^campany/modify/(?P<tid>[0-9]+)/$', modifyCampany),
    url(r'^campany/create/$', createCampany),
    url(r'^campany/start/(?P<tid>[0-9]+)/$', startCampany),
    url(r'^campany/stop/(?P<tid>[0-9]+)/$', stopCampany),
    url(r'^replenish/detail/(?P<tid>[0-9]+)/$', replenish_detail),
    url(r'^replenish/set_payed/(?P<tid>[0-9]+)/$', replenish_set_payed),
    url(r'^replenish/$', replenish),
    url(r'^', index)
]
