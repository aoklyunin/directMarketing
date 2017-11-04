# форма оборудования
from django.forms import ModelForm, ChoiceField, TextInput, forms, Textarea, FileInput

from customer.models import MarketCamp


class MarketCampForm(ModelForm):
    platform = ChoiceField(label='Платформа')

    class Meta:
        model = MarketCamp
        fields = {'description', 'viewPrice', 'budget', 'image', 'startTime', 'endTime','vkPostID'}
        widgets = {
            'description': Textarea(),
            'viewPrice': TextInput(attrs={}),
            'budget': TextInput(attrs={}),
            'image': FileInput(),
        }

        labels = {
            'description': 'Текст',
            'viewPrice': 'Цена просмотра',
            'budget': 'Бюджет',
            'startTime': 'Старт кампании',
            'endTime': 'Конец кампании',
            'image': 'Картинка кампании',
            'vkPostID': 'ID поста',
        }

        error_messages = {
            'name': {'required': 'Это поле обязательно'},
            'viewPrice': {'required': 'Это поле обязательно'},
            'budget': {'required': 'Это поле обязательно'},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(MarketCampForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now

        self.fields['platform'].choices = MarketCamp.PLATFORM_CHOICES
        self.fields['image'].required = False
        self.fields['startTime'].widget.attrs['id'] = 'startTime'
        self.fields['endTime'].widget.attrs['id'] = 'endTime'
        self.fields['endTime'].widget.attrs['class'] = 'form_datetime'
        self.fields['vkPostID'].required = False
