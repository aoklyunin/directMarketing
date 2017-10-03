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
        for task in Task.objects.filter(pub_date__lt=datetime.date.today() - datetime.timedelta(days=15)):
            # for task in Task.objects.all():
            print(task.task_name)
            for m in Mark.objects.filter(task=task):
                #print(m)
                m.sources.all().clear()
            Mark.objects.filter(task=task).delete()
            for p in PretendToCheat.objects.filter(task=task):
                p.vals.all().delete()
                print p
            PretendToCheat.objects.filter(task=task).delete()



