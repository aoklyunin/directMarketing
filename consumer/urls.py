from django.conf.urls import url

from consumer.views import balance, campanies, index, terms, detailCampany, leaveCampany, joinCampany, withdraw_detail, \
    withdraw, autoWithdraw, loginVK, vkTest, vkLink

urlpatterns = [

    url(r'^balance/$', balance),
    url(r'^campanies/(?P<tp>[0-9])/$', campanies),
    url(r'^campany/join/(?P<tid>[0-9]+)/$', joinCampany),
    url(r'^campany/leave/(?P<tid>[0-9]+)/$', leaveCampany),
    url(r'^campany/detail/(?P<tid>[0-9]+)/$', detailCampany),
    url(r'^withdraw/detail/(?P<tid>[0-9]+)/$', withdraw_detail),
    url(r'^withdraw/$', withdraw),
    url(r'^withdraw/auto/(?P<tp>[0-9])/$', autoWithdraw),
    url(r'^terms/$', terms),
    url(r'^login/vk/$', loginVK),
    url(r'^vktest/$', vkTest),
    url(r'^vklink/$', vkLink),
    url(r'^', index)
]
