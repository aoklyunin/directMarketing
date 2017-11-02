# -*- coding: utf-8 -*-
from adminPanel.models import AdminUser
from consumer.models import Consumer
from customer.models import Customer


def getUsType(user):
    try:
        Customer.objects.get(user=user)
        return 1
    except:
        try:
            Consumer.objects.get(user=user)
            return 2
        except:
            try:
                AdminUser.objects.get(user=user)
                return 3
            except:
                return 0