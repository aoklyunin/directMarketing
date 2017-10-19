# форма оборудования
from django.forms import ModelForm, ChoiceField, TextInput, forms, Textarea

from customer.models import MarketCamp


class MarketCampForm(ModelForm):
    platform = ChoiceField(label='Платформа')

    class Meta:
        model = MarketCamp
        fields = {'description', 'viewPrice', 'budget','image'}
        widgets = {
            'description': Textarea(),
            'viewPrice': TextInput(attrs={}),
            'budget': TextInput(attrs={}),

        }

        labels = {
            'description': 'Текст',
            'viewPrice': 'Цена просмотра',
            'budget': 'Бюджет',
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
        self.fields['image'].upload_to = '/pictures/'
        self.fields['image'].required = False



