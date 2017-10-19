from django.contrib import admin

# Register your models here.
from customer.models import Customer, MarketCamp, ReplenishTransaction

admin.site.register(Customer)
admin.site.register(MarketCamp)
admin.site.register(ReplenishTransaction)