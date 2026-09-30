from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from tracker.models import Transaction
from .models import Transaction, Budget
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'category', 'amount', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
        from .models import Budget
import datetime

MONTH_CHOICES = [(i, datetime.date(2000, i, 1).strftime('%B')) for i in range(1, 13)]

class BudgetForm(forms.ModelForm):
    month = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Budget
        fields = ['month', 'year', 'amount']
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 2020, 'max': 2100}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }