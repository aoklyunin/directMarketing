from django.conf.urls import url

from consumer.views import balance, campanies, index, terms, detailCampany, leaveCampany, joinCampany, withdraw_detail, \
    withdraw, autoWithdraw, loginVK, vkProcess, vkProcessR, postVKview

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
    url(r'^vk/getToken/$', loginVK),
    url(r'^vk/processAnswer/(?P<user_id>[0-9]+)/(?P<access_token>[0-9a-zA-Z]+)/$', vkProcess),
    url(r'^vk/processAnswerR/$', vkProcessR),
    url(r'^vk/post/$', postVKview),
    url(r'^', index)
]
