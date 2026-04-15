from django.core.exceptions import ValidationError
from datetime import date

from django import forms

from rentingsystem.models import Payment
from .models import Vehicle,Booking

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        price_per_day = cleaned_data.get('price_per_day')

        if price_per_day is not None and price_per_day <= 0:
            raise ValidationError("Price must be greater than 0")

        return cleaned_data

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'user',
            'vehicle',
            'start_date',
            'end_date',
            'status'
        ]
   
    
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'