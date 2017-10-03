# coding=utf-8
# программа для загрузки оценок
import datetime

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from localCode.moodle import MoodleHelper
from sworks.models import Student, Task, Mark, TaskType, ProgramCode, CodeLanguage, PretendToCheat


# описание класса програмы
class Command(BaseCommand):
    # описание программы
    helf = 'load all attempts'

    def handle(self, *args, **options):
        # проходим по всем заданиям за последние 30 дней
        ps = PretendToCheat.objects.filter(state=0)
        for p in ps:
            p.vals.all().delete()




