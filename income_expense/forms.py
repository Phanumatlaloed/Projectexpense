from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'description', 'category', 'amount', 'transaction_type']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'Select a date'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a description'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a category (e.g., Food, Transport)'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the amount'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'date': 'Transaction Date',
            'description': 'Description',
            'category': 'Category',
            'amount': 'Amount',
            'transaction_type': 'Type of Transaction',
        }
