from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class AdminUser(models.Model):
    # пользователь
    user = models.OneToOneField(User)