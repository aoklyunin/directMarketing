from django.conf.urls import url

from consumer.views import balance, campanies, index, terms, detailCampany, leaveCamapany, joinCampany, withdraw_detail, \
    withdraw_set_payed, withdraw

urlpatterns = [

    url(r'^balance/$', balance),
    url(r'^campanies/(?P<tp>[0-9])/$', campanies),
    url(r'^campany/join/(?P<tid>[0-9]+)/$', joinCampany),
    url(r'^campany/leave/(?P<tid>[0-9]+)/$', leaveCamapany),
    url(r'^campany/detail/(?P<tid>[0-9]+)/$', detailCampany),
    url(r'^withdraw/detail/(?P<tid>[0-9]+)/$', withdraw_detail),
    url(r'^withdraw/set_payed/(?P<tid>[0-9]+)/$', withdraw_set_payed),
    url(r'^withdraw/$', withdraw),
    url(r'^terms/$', terms),
    url(r'^', index)
]
