from django import forms
from .models import Account

from .models import Transaction

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['source', 'destination', 'amount']
        widgets = {
            'source': forms.Select(attrs={
                'class': 'form-select block w-full mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'destination': forms.Select(attrs={
                'class': 'form-select block w-full mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-input block w-full mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            })
        }
    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get("source")
        destination = cleaned_data.get("destination")
        amount = cleaned_data.get("amount")

        if source and destination and amount:
            if source == destination:
                raise forms.ValidationError("Source and destination accounts must be different.")
            if not source.can_withdraw(amount):
                raise forms.ValidationError("Insufficient funds in the source account.")
