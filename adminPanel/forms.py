

# форма для выбора одного изделия с кол-вом
from django.forms import Form, IntegerField, CharField, HiddenInput


class ConsumerViewsForm(Form):
    link = CharField(label="")
    cnt = IntegerField(label="")
    id = IntegerField(label="")

    def __init__(self, *args, **kwargs):
        super(ConsumerViewsForm, self).__init__(*args, **kwargs)

        self.fields['cnt'].initial = 0
        self.fields['link'].required = False
        self.fields['id'].required = False
        self.fields['link'].widget = HiddenInput()
        self.fields['id'].widget = HiddenInput()
