from django import forms
from .models import Booking, Payment,Profile
from django.contrib.auth.models import User


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_end_date(self):
     end_date = self.cleaned_data.get('end_date')
     start_date = self.cleaned_data.get('start_date')

     if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be before start date.")

     return end_date

class PaymentForm(forms.ModelForm):
    
    mark_paid = forms.BooleanField(required=False, label='Mark as Paid')

    class Meta:
        model = Payment
        fields = ['method', 'transaction_id']

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    class Meta:
            model = Profile
            fields = ['phone', 'address', 'location']

    def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
            if self.user:
                self.fields['first_name'].initial = self.user.first_name
                self.fields['last_name'].initial = self.user.last_name
                self.fields['email'].initial = self.user.email

    def save(self, commit=True):
            profile = super().save(commit=False)
            if self.user:
                self.user.first_name = self.cleaned_data['first_name']
                self.user.last_name = self.cleaned_data['last_name']
                self.user.email = self.cleaned_data['email']
                self.user.save()
            if commit:
                profile.save()
            return profile
