# -*- coding: utf-8 -*-
# модуль с формами
from django import forms

from sworks.models import Task


# форма добавления попытки
class AddAttemptForm(forms.Form):
    # задание
    task = forms.ModelChoiceField(queryset=Task.objects.all(), empty_label="Выберите задание", label="")
    # первый комментарий
    comment = forms.CharField(max_length=100000,
                              widget=forms.Textarea(attrs={'rows': 4, 'cols': 90, 'placeholder': 'Комментарий'}),
                              label="")
    # ссылка на попытку
    link = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': 'Ссылка'}), label="")


# форма для просмотра своей попытки
class AttemptForm(forms.Form):
    text = forms.CharField(max_length=100000,
                           widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Ссылка'}), label="")


# форма для просмотра своей попытки
class FloatForm(forms.Form):
    val = forms.FloatField()


# форма добавления задания
class AddTaskForm(forms.Form):
    # имя задания
    task_name = forms.CharField(max_length=200,
                                widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': 'название задания'}),
                                label="Название задания ")
    # дата выдачи
    pub_date = forms.CharField(max_length=200,
                               widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}),
                               label="Дата опубликовая")


# форма логина
class LoginForm(forms.Form):
    # имя пользователя
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Логин'}),
                               label="")
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label="")

    widgets = {
        'password': forms.PasswordInput(),
    }


# форма регистрации
class RegisterForm(forms.Form):
    # логин
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'mylogin'}),
                               label="Логин")
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
                               label="Пароль")
    # повтор пароля
    rep_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
        label="Повторите пароль")
    # класс
    github_rep = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 20, 'placeholder': 'https://github.com/aoklyunin/csi-students'}),
                                 label="Ссылка на github репозиторий")
    # группа
    st_group = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'P4135'}),
                               label="номер группы")
    # почта
    mail = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'example@gmail.com'}),
                           label="Адрес эл. почты")
    # имя
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иван'}), label="Имя")
    # фамилия
    second_name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иванов'}),
                                  label="Фамилия")


# форма для оценки
class MarkForm(forms.Form):
    # оценка
    mark = forms.CharField(max_length=1,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 2}),
                           label="")
