from django.conf.urls import url

from consumer.views import campanies, index, detailCampany, withdrawDetail, \
    withdraw,campaniesList
from consumer.vkViews import getCode, processCode, postVKview

urlpatterns = [
    url(r'^withdraw/detail/(?P<tid>[0-9]+)/$', withdrawDetail),
    url(r'^withdraw/$', withdraw),
    url(r'^vk/getCode/$', getCode),
    url(r'^vk/processCode/$', processCode),
    url(r'^vk/post/$', postVKview),
    url(r'^campanies/$', campanies),
    url(r'^campanies/(?P<tp>[0-9])/$', campaniesList),
    url(r'^campany/detail/(?P<tid>[0-9]+)/$', detailCampany),
    url(r'^', index)
]
