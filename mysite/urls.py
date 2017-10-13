# -*- coding: utf-8 -*-
# обработчик адресов сайта
from django.conf.urls import include, url
from django.contrib import admin
import mainApp.staticViews
import mainApp.auth
import mainApp.views
import mainApp.transactionViews

# автоопределение администратора
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', mainApp.staticViews.about),
    url(r'^customer/$', mainApp.staticViews.customer),
    url(r'^consumer/$', mainApp.staticViews.consumer),
    url(r'^contact/$', mainApp.staticViews.contact),
    url(r'^signin/$', mainApp.auth.signin),
    url(r'^signup/$', mainApp.auth.signup),
    url(r'^signout/$', mainApp.auth.signout),
    url(r'^signup/consumer/$', mainApp.auth.signup_consumer),
    url(r'^signup/customer/$', mainApp.auth.signup_customer),
    url(r'^customer_terms/$', mainApp.staticViews.customer_terms),
    url(r'^consumer_terms/$', mainApp.staticViews.consumer_terms),
    url(r'^personal/main/$', mainApp.views.personal_main),
    url(r'^personal/balance/$', mainApp.views.personal_balance),
    url(r'^personal/marketing/$', mainApp.views.personal_marketing),
    url(r'^transactions/replenish/$', mainApp.transactionViews.replenish),
    url(r'^transactions/withdraw/$', mainApp.transactionViews.withdraw),
    url(r'^transactions/customer_detail/(?P<tid>[0-9])/$', mainApp.transactionViews.customer_detail),
    url(r'^transactions/customer_transaction_set_user_payed/(?P<tid>[0-9])/$', mainApp.transactionViews.customer_transaction_set_user_payed),
    url(r'^replenish/admin/$', mainApp.transactionViews.replanishAdmin),
    url(r'^replenish/admin/reject/(?P<tid>[0-9])/$', mainApp.transactionViews.replanishAdminReject),
    url(r'^replenish/admin/accept/(?P<tid>[0-9])/$', mainApp.transactionViews.replanishAdminAccept),
    url(r'^replenish/admin/complete/$', mainApp.transactionViews.replanishAdminComplete),
    url(r'^replenish/admin/rejected/$', mainApp.transactionViews.replanishAdminRejected),
    url(r'^replenish/admin/not-complete/$', mainApp.transactionViews.replanishAdminNotComplete),
    url(r'^withdraw/admin/$', mainApp.transactionViews.withdrawAdmin),
    url(r'^', mainApp.staticViews.index, name='index')
]
