from django.contrib import admin

# Register your models here.
from consumer.models import ConsumerMarketCamp, Consumer, WithdrawTransaction

admin.site.register(Consumer)

admin.site.register(ConsumerMarketCamp)
admin.site.register(WithdrawTransaction)

