from django import forms
from .models import Reservation
from django.forms import ModelForm

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'check_in_date', 'check_out_date']
