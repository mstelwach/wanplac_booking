from django import forms
from django.forms import inlineformset_factory, TextInput, Select

from reservation.models import Reservation, ReservationDetail, Kayak


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
        exclude = ['user', 'status', 'created']
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Imię potrzebne do rezerwacji'}),
            'last_name': TextInput(attrs={'placeholder': 'Nazwisko potrzebne do rezerwacji'}),
            'date': TextInput(attrs={'placeholder': 'Data rezerwacji'}),
            'time': TextInput(attrs={'placeholder': 'Godzina rezerwacji'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationCreateUpdateForm, self).__init__(*args, **kwargs)
        self.fields['route'].empty_label = 'Wybierz szlak'


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 100)]


class ReservationDetailForm(forms.ModelForm):

    class Meta:
        model = ReservationDetail
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ReservationDetailForm, self).__init__(*args, **kwargs)
        self.fields['kayak'].widget = SelectWidget(attrs={},
                                                   choices=[('', 'Wybierz kajak')] + [(str(kayak.pk), kayak) for kayak in Kayak.objects.all()],
                                                   )
        self.fields['kayak'].widget.disabled_choices = [str(kayak.id) for kayak in Kayak.objects.filter(available=False)]
        self.fields['kayak'].is_required = True
        # self.fields['quantity'] = forms.ChoiceField(choices=PRODUCT_QUANTITY_CHOICES)

    def clean_kayak(self):
        data = self.cleaned_data['kayak']
        if not data:
            raise forms.ValidationError('This field is required')
        return data


ReservationKayakFormSet = inlineformset_factory(
    Reservation, ReservationDetail, form=ReservationDetailForm,
    fields=['kayak', 'quantity'], extra=1, can_delete=True, error_messages='This field is required'
)

