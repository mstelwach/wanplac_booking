from django import forms
from django.forms import inlineformset_factory, TextInput, Select, BaseInlineFormSet
from reservation.models import Reservation, ReservationDetail, Kayak, PAYMENT_METHOD


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


class ReservationCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Reservation
        exclude = ['user', 'status', 'created', 'paid', 'currency']
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Imię potrzebne do rezerwacji'}),
            'last_name': TextInput(attrs={'placeholder': 'Nazwisko potrzebne do rezerwacji'}),
            'date': TextInput(attrs={'placeholder': 'Data rezerwacji'}),
            'time': TextInput(attrs={'placeholder': 'Godzina rezerwacji'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationCreateUpdateForm, self).__init__(*args, **kwargs)
        self.fields['route'].empty_label = 'Wybierz szlak'
        self.fields['payment'] = forms.ChoiceField(choices=PAYMENT_METHOD,
                                                   widget=forms.RadioSelect(attrs={'id': 'value'}))


class ReservationDetailForm(forms.ModelForm):

    class Meta:
        model = ReservationDetail
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ReservationDetailForm, self).__init__(*args, **kwargs)
        qs_kayaks_all = [(str(kayak.pk), kayak) for kayak in Kayak.objects.all()]
        self.fields['kayak'].widget = SelectWidget(attrs={},
                                                   choices=[('', 'Wybierz kajak')] + qs_kayaks_all,
                                                   )
        qs_kayaks_not_available = [str(kayak.id) for kayak in Kayak.objects.filter(available=False)]
        self.fields['kayak'].widget.disabled_choices = [''] + qs_kayaks_not_available
        self.fields['quantity'] = forms.ChoiceField(choices=[(0, '---------')])

        for counter in range(len(Kayak.objects.all())):
            if 'details-{}-kayak'.format(counter) in self.data:
                kayak_pk = self.data.get('details-{}-kayak'.format(counter))
                kayak = Kayak.objects.get(pk=kayak_pk)
                self.fields['quantity'].choices = [(number, number) for number in range(1, kayak.stock + 1)]


ReservationKayakFormSet = inlineformset_factory(Reservation,
                                                ReservationDetail,
                                                form=ReservationDetailForm,
                                                extra=1,
                                                can_delete=True
                                                )


