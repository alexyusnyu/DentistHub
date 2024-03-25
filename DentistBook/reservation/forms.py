from django import forms
from .models import Reservation


class DentistsofficeServiceForm(forms.Form):
    service = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        services = kwargs.pop('services')
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = services


class DentistsofficeDentistForm(forms.Form):
    dentist = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        dentists = kwargs.pop('dentists')
        super().__init__(*args, **kwargs)
        self.fields['dentist'].queryset = dentists


class DateSelectionForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
        label='Select Date'
    )


class TimeSelectionForm(forms.Form):
    time_slot = forms.ChoiceField(label='Select Time Slot', choices=())

    def __init__(self, *args, **kwargs):
        time_slot_choices = kwargs.pop('choices', ())
        super().__init__(*args, **kwargs)
        self.fields['time_slot'].choices = time_slot_choices


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('user', 'dentistsoffice', 'service', 'dentist', 'date', 'time')
        widgets = {
            'user': forms.HiddenInput(),
            'dentistsoffice': forms.HiddenInput(),
            'service': forms.HiddenInput(),
            'dentist': forms.HiddenInput(),
            'date': forms.HiddenInput(),
            'time': forms.HiddenInput(),
        }

