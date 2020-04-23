from django import forms
from django.forms import inlineformset_factory, TextInput, Select
from reservation.models import Reservation, ReservationDetail, Kayak, PAYMENT_METHOD, StockDateKayak


class SelectWidget(Select):
    """
    Subclass of Django's select widget that allows disabling options.
    """
    def __init__(self, *args, **kwargs):
        self._disabled_choices = []
        super(SelectWidget, self).__init__(*args, **kwargs)

    @property
    def disabled_choices(self):
        return self._disabled_choices

    @disabled_choices.setter
    def disabled_choices(self, other):
        self._disabled_choices = other

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option_dict = super(SelectWidget, self).create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        if value in self.disabled_choices:
            option_dict['attrs']['disabled'] = 'disabled'
        return option_dict


class ReservationCreateForm(forms.ModelForm):

    class Meta:
        model = Reservation
        exclude = ['user', 'status', 'created', 'paid', 'currency']
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Imię potrzebne do rezerwacji'}),
            'last_name': TextInput(attrs={'placeholder': 'Nazwisko potrzebne do rezerwacji'}),
            'date': TextInput(attrs={'placeholder': 'Data rezerwacji'}),
            'time': TextInput(attrs={'placeholder': 'Godzina rezerwacji'}),
        }
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'date': 'Data',
            'time': 'Godzina',
            'phone': 'Telefon',
            'route': 'Trasa'
        }
        help_texts = {
            'first_name': 'Pozostaw puste pole, jeżeli chcesz aby rezerwacja została dokonana na twoje imię.',
            'last_name': 'Pozostaw puste pole, jeżeli chcesz aby rezerwacja została dokonana na twoje nazwisko.'
        }

    def __init__(self, *args, **kwargs):
        super(ReservationCreateForm, self).__init__(*args, **kwargs)
        self.fields['route'].empty_label = 'Wybierz'
        self.fields['payment'] = forms.ChoiceField(choices=PAYMENT_METHOD,
                                                   widget=forms.RadioSelect(attrs={'id': 'value'}))


class ReservationDetailForm(forms.ModelForm):

    class Meta:
        model = ReservationDetail
        exclude = ()
        labels = {
            'kayak': 'Kajak',
            'quantity': 'Ilość'
        }
        widgets = {
            'kayak': Select(attrs={
                'onchange': 'validateKayak(this);'
            }),
            'quantity': Select(attrs={
                'onchange': 'validateQuantity(this);',
                'disabled': 'disabled'
            })
        }

    def __init__(self, *args, **kwargs):
        super(ReservationDetailForm, self).__init__(*args, **kwargs)
        self.fields['kayak'].queryset = Kayak.objects.none()
        self.fields['kayak'].empty_label = 'Musisz wybrać datę'

        if 'date' in self.data:
            date = self.data.get('date')
            self.fields['kayak'].queryset = Kayak.objects.filter(stockdatekayak__date=date)

            self.fields['quantity'] = forms.ChoiceField(choices=[(0, '-------')])
            for counter in range(len(Kayak.objects.all())):
                if 'details-{}-kayak'.format(counter) in self.data and self.data['details-{}-kayak'.format(counter)]:
                    kayak_pk = int(self.data.get('details-{}-kayak'.format(counter)))
                    kayak = Kayak.objects.get(pk=kayak_pk)
                    stock_date_kayak = StockDateKayak.objects.get(kayak=kayak, date=date)
                    self.fields['quantity'].choices = [(number, number) for number in range(1,
                                                                                            stock_date_kayak.stock + 1)]


ReservationKayakFormSet = inlineformset_factory(Reservation,
                                                ReservationDetail,
                                                form=ReservationDetailForm,
                                                extra=1,
                                                can_delete=True
                                                )


class ReservationUpdateForm(forms.ModelForm):

    class Meta:
        model = Reservation
        exclude = ['user', 'status', 'created', 'paid', 'currency', 'payment']
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Imię potrzebne do rezerwacji'}),
            'last_name': TextInput(attrs={'placeholder': 'Nazwisko potrzebne do rezerwacji'}),
            'date': TextInput(attrs={'placeholder': 'Data rezerwacji'}),
            'time': TextInput(attrs={'placeholder': 'Godzina rezerwacji'}),
        }
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'date': 'Data',
            'time': 'Godzina',
            'phone': 'Telefon',
            'route': 'Trasa'
        }
        help_texts = {
            'first_name': 'Pozostaw puste pole, jeżeli chcesz aby rezerwacja została dokonana na twoje imię.',
            'last_name': 'Pozostaw puste pole, jeżeli chcesz aby rezerwacja została dokonana na twoje nazwisko.'
        }

    def __init__(self, *args, **kwargs):
        super(ReservationUpdateForm, self).__init__(*args, **kwargs)
        self.fields['route'].empty_label = 'Wybierz'
