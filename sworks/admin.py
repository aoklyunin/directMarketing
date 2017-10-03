# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Student, Task, AttemptComment, Mark, InfoText

admin.site.register(Student)
admin.site.register(Task)
admin.site.register(AttemptComment)

# если нужно сделать своё представление модели в админке, нужно убрать её регистрацию из списка выше

UserAdmin.list_display = ('email', 'first_name', 'last_name', 'is_staff', 'username')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Mark)
admin.site.register(InfoText)