# coding=utf-8
# программа для загрузки оценок
import datetime

import itertools
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from localCode.codeAnalysis import SimpleCodeAnalysis
from localCode.moodle import MoodleHelper
from sworks.models import Student, Task, Mark, TaskType, ProgramCode, CodeLanguage, PretendVal, PretendToCheat


# описание класса програмы
class Command(BaseCommand):
    # получаем двумерный массив первая координата - оценка, вторая - номер программы в оценке
    # возвращает массив и длину строк в нём
    def generateCodeDataFromMarks(self, marks):
        data = []
        ln = 0
        for m in marks:
            # m.checked = True
            # m.save()
            ar = []
            for source in m.sources.all():
                ar.append(SimpleCodeAnalysis(source))
            l = len(ar)
            if ln == 0 and l != 0:
                ln = l
            data.append(ar)
        # если программных кодов нет, то заполняем исходники пустыми строками
        for d in data:
            if (len(d)) == 0:
                for i in range(ln):
                    d.append(
                        SimpleCodeAnalysis(ProgramCode.objects.create(language=CodeLanguage.objects.all().first(),
                                                                      text="")))
        return (data, ln)

    # описание программы
    helf = 'checkCodes'

    def handle(self, *args, **options):
        # экземпляр класса для работы с mdl
        moodle = MoodleHelper()
        # проходим по всем заданиям за последние 30 дней

        tt = TaskType.objects.get(name="Программирование")
        for task in Task.objects.filter(task_type=tt).filter(
                pub_date__gt=datetime.date.today() - datetime.timedelta(days=60)):
            # for task in Task.objects.all():
            print(task.task_name)
            # try:
            marks = Mark.objects.filter(checked=0).filter(task=task)
            # print(marks)
            (add_data, ln) = self.generateCodeDataFromMarks(marks)
            if (len(add_data) == 0):
                print "в этом задании нет непроверенных оценок"
                continue
            marks.update(checked=1)
            # надо добавить фильтр по непроверенным оценкам
            marks = Mark.objects.filter(task=task)
            (all_data, ln) = self.generateCodeDataFromMarks(marks)

            for i in range(ln):
                try:
                    arr = []
                    for j in range(len(all_data)):
                        arr.append(all_data[j][i])
                    arr_add = []
                    for j in range(len(add_data)):
                        arr_add.append(add_data[j][i])

                    lstAdd = []
                    for a, b in [(x, y) for x in arr for y in arr_add if x != y]:
                        if a.sorceCode != b.sorceCode:
                            c = a.compaireTo(b)
                            #print(c)
                            if c > 85:
                                lstAdd.append([a,b,c])

                    for rec in lstAdd:
                        print "begin"
                        print rec[2]
                        pVal = PretendToCheat.objects.create(task=task, state=0, n=i)
                        pVal.save()
                        for r in rec[:-1]:
                            m = Mark.objects.filter(sources=r.sorceCode).first()
                            print (r.sorceCode.link)
                            student = Student.objects.filter(marks=m).first()
                            p = PretendVal.objects.create(programCode=r.sorceCode, mark=m, student=student)
                            p.unique = rec[2]

                            p.save()
                            pVal.vals.add(p)
                        print "end"
                    # for d in data:
                    #   print(len(d[0]))



                except:
                       pass
