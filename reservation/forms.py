from django import forms
from django.forms import inlineformset_factory, TextInput
from reservation.models import Reservation, ReservationItem


class ReservationCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Reservation
        exclude = ['user']
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Imię potrzebne do rezerwacji'}),
            'last_name': TextInput(attrs={'placeholder': 'Nazwisko potrzebne do rezerwacji'}),
            'term': TextInput(attrs={'placeholder': 'Data rezerwacji'}),
            'time': TextInput(attrs={'placeholder': 'Godzina rezerwacji'}),
        }


class ReservationItemForm(forms.ModelForm):

    class Meta:
        model = ReservationItem
        exclude = ['reservation']


ReservationKayakFormSet = inlineformset_factory(
    Reservation, ReservationItem, form=ReservationItemForm,
    fields=['kayak', 'quantity'], extra=1, can_delete=True
)

