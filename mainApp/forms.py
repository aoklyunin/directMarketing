# -*- coding: utf-8 -*-
# модуль с формами
from django import forms



# форма регистрации
class RegisterConsumerForm(forms.Form):
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
                               label="Пароль")
    # повтор пароля
    rep_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
        label="Повторите пароль")

    # почта
    mail = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'example@gmail.com'}),
                           label="Адрес эл. почты")

    acceptedTerms = forms.BooleanField(label="Я ознакомлен с <a href='/consumer_terms/'>Условиями</a>")


# форма регистрации
class RegisterCustomerForm(RegisterConsumerForm):
    # имя
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Генри'}), label="Имя")
    # фамилия
    second_name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Форд'}),
                                  label="Фамилия")
    # почта
    mail = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'henry@ford.com'}),
                           label="Адрес эл. почты")

    acceptedTerms = forms.BooleanField(label="Я ознакомлен с <a href='/customer_terms/'>Условиями</a>")


# форма регистрации
class CustomerForm(forms.Form):
    # имя
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Space X'}),
                           label="Название компании")
    # киви кошелёк
    qiwi = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': '+7 999 888 77 66'}),
                           label="Киви-кошелёк")



# форма логина
class LoginForm(forms.Form):
    # имя пользователя
    login = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Адрес почты'}),
                            label="")
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label="")

    widgets = {
        'password': forms.PasswordInput(),
    }


# форма логина
class PaymentForm(forms.Form):
    # имя пользователя
    value = forms.FloatField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': '100.00'}),
                             label="Cумма")


# форма логина
class TextForm(forms.Form):
    # имя пользователя
    value = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 20, 'placeholder': 'введите вопрос'}),
                            label="")

# форма логина
class PostIdForm(forms.Form):
    # имя пользователя
    id = forms.IntegerField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'введите id'}),
                            label="id записи")



a = '''
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





# форма для оценки
class MarkForm(forms.Form):
    # оценка
    mark = forms.CharField(max_length=1,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 2}),
                           label="")
                           
'''
