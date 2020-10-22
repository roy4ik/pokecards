from django import forms
from .models import Trade, Vault
from .tcg import shuffle_return7

class Trade_offer(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['cards','public']
        widgets = {
            'cards': forms.CheckboxSelectMultiple()
        }