from django import forms

# форма регистрации
class ConsumerForm(forms.Form):
    # имя
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Илон'}),
                           label="Имя")
    # имя
    second_name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Маск'}),
                                  label="Фамилия")

    # киви кошелёк
    qiwi = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': '+7 999 888 77 66'}),
                           label="Киви-кошелёк")

    # автоматическое участие
    autoParticipate = forms.BooleanField(label="Автоматическое участие",required=False)