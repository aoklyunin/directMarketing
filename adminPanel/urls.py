from django.conf.urls import url

from adminPanel.views import *

urlpatterns = [
    url(r'^replenish/$', replenish),
    url(r'^replenish/list/(?P<state>[0-9]+)/$', replenishList),
    url(r'^withdraw/$', withdraw),
    url(r'^withdraw/list/(?P<state>[0-9]+)/$', withdrawList),
    url(r'^replenish/reject/(?P<tid>[0-9]+)/$', replenishReject),
    url(r'^replenish/accept/(?P<tid>[0-9]+)/$', replenishAccept),
    url(r'^withdraw/reject/(?P<tid>[0-9]+)/$', withdrawReject),
    url(r'^withdraw/accept/(?P<tid>[0-9]+)/$', withdrawAccept),
    url(r'^campany/dismiss/(?P<tid>[0-9]+)/$', dismissCampany),
    url(r'^cheaters/$', cheaters),
    url(r'^cheaters/list/(?P<cheated>[0-9]+)/$', listCheater),
    url(r'^cheaters/punish/(?P<c_id>[0-9]+)/$', punishCheater),
    url(r'^cheaters/free/(?P<c_id>[0-9]+)/$', freeCheater),
    url(r'^blocked/list/$', listBlocked),
    url(r'^blocked/free/(?P<c_id>[0-9]+)/$', freeBlocked),

   # url(r'^', index, name='index')
]
