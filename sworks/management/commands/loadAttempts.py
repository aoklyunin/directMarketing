# coding=utf-8
# программа для загрузки оценок
import datetime

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from localCode.moodle import MoodleHelper
from sworks.models import Student, Task, Mark, TaskType, ProgramCode, CodeLanguage


# по заданию и кол-ву баллов получить оценку
def getValBySum(task, cnt):
    s = str(int(cnt))
    if s in task.est1:
        return int(1)
    elif s in task.est2:
        return int(2)
    elif s in task.est3:
        return int(3)
    elif s in task.est4:
        return int(4)
    elif s in task.est5:
        return int(5)
    else:
        return int(0)


# описание класса програмы
class Command(BaseCommand):
    # описание программы
    helf = 'load all attempts'

    def handle(self, *args, **options):
        # экземпляр класса для работы с mdl
        moodle = MoodleHelper()
        # проходим по всем заданиям за последние 30 дней
        for task in Task.objects.filter(pub_date__gt=datetime.date.today() - datetime.timedelta(days=60)):
            # for task in Task.objects.all():
            print(task.task_name)
            try:
                # тип задания: программирование или эссе
                tt = TaskType.objects.get(name="Программирование")
                # загружаем попытку
                attempts = moodle.loadAttempts(task.task_name, task.task_type == tt)
                # проходим по загруженным попыткам
                for at in attempts:
                    # ищем соотв. пользователя
                    user = User.objects.filter(first_name=at["name"], last_name=at["second_name"]).first()
                    # если такой пользователь есть
                    if user:
                        # ищем соотв. ему студента
                        student = Student.objects.filter(user=user).first()
                        # если студент найден
                        if student:
                            # получаем оценку по сумме
                            val = round(at["sum"])
                            #print(str(val)+" "+str(at["sum"]))
                            flgAddCode = False
                            # ищем оценку этого студента за выбранное задание
                            m = student.marks.filter(task=task).first()
                            # если оценка уже есть
                            if m:
                                # если новая оценка больше текущей
                                if m.m_value!=-1 and val > m.m_value:
                                    # меняем оценку
                                    m.m_value = round(at["sum"])
                                    # меняем ссылку
                                    m.link = at["href"]
                                    for s in m.sources.all():
                                        s.delete()

                                    m.sources.clear()
                                    # сохраняем изменения
                                    m.save()
                                    flgAddCode = True
                            else:
                                # создаём новую оценку
                                m = Mark.objects.create(task=task, m_value=val, link=at["href"])
                                # сохраняем оценку
                                m.save()
                                # добавляем оценку студенту
                                student.marks.add(m)
                                flgAddCode = True

                            if task.task_type ==tt and (flgAddCode or (m and not m.sources.all())):
                                i = 0
                                for code in moodle.loadCodeFromAttempt(at["href"]):
                                    #print(len(code[0]))
                                    i=i+1
                                    pg = ProgramCode.objects.create(language = CodeLanguage.objects.get(name="Java"),
                                                                    n = i)
                                    pg.text = code[0]
                                    pg.link = code[1]
                                    pg.save()
                                    m.sources.add(pg)

            except:
                pass
