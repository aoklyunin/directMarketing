from django.conf.urls import url

from adminPanel.replenishViews import *
from adminPanel.views import *
from adminPanel.withdrawViews import *

urlpatterns = [
    url(r'^replenish/$', replenish),
    url(r'^campanies/$', campanies),
    url(r'^campany/detail/(?P<tid>[0-9]+)/$', detailCampany),
    url(r'^campany/approve/(?P<tid>[0-9]+)/$', approveCampany),
    url(r'^campany/dismiss/(?P<tid>[0-9]+)/$', dismissCampany),
    url(r'^replenish/reject/(?P<tid>[0-9]+)/$', replenishReject),
    url(r'^replenish/accept/(?P<tid>[0-9]+)/$', replenishAccept),
    url(r'^replenish/accepted/$', replanishAccepted),
    url(r'^replenish/rejected/$', replenishRejected),
    url(r'^replenish/not-accepted/$', replenishNotAccepted),
    url(r'^withdraw/$', withdraw),

    url(r'^', index, name='index')
]
