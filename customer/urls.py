from django.conf.urls import url

from customer.views import balance, campanies, index, replenish, replenish_detail, terms, replenish_set_payed

urlpatterns = [
    url(r'^balance/$', balance),
    url(r'^campanies/$', campanies),
    url(r'^replenish/$', replenish),
    url(r'^replenish_detail/(?P<tid>[0-9])/$', replenish_detail),
    url(r'^replenish_set_payed/(?P<tid>[0-9])/$', replenish_set_payed),
    url(r'^terms/$', terms),

    url(r'^', index, name='index')
]
